from datetime import datetime, timedelta
from test_runners import single_test_runner
from methods import *
import matplotlib.pyplot as plt
import matplotlib.style as style

FORMAT = '%d-%m-%Y %H:%M:%S'


def trend_test(n, min_duplicates=0, max_duplicates=100, interval_value=10, trials=5):
    result_dict = {
        'pandas.to_datetime with specified format': dict(),
        'time.strptime with memoization': dict(),
        'pre-built lookup mapping': dict()}

    duplicates_count = min_duplicates

    while duplicates_count <= max_duplicates:
        ts_list = _create_uniform_known_format_timestamps_with_duplicates(n, duplicates=duplicates_count)
        result_dict['time.strptime with memoization'][duplicates_count] = single_test_runner(
            apply_strptime_with_memos,
            data_list=ts_list,
            trials=trials,
            format=FORMAT)

        result_dict['pandas.to_datetime with specified format'][duplicates_count] = single_test_runner(
            apply_pd_to_datetime,
            data_list=ts_list,
            trials=trials,
            infer=True,
            format=FORMAT,
            split=duplicates_count + 1)

        result_dict['pre-built lookup mapping'][duplicates_count] = single_test_runner(
            apply_prebuilt_memos,
            data_list=pd.Series(ts_list),
            trials=trials,
            format=FORMAT,
            start_time=datetime(2000, 1, 1),
            end_time=datetime(2000, 1, 1) + timedelta(seconds=(n / (duplicates_count + 1))))

        duplicates_count += interval_value

    print(result_dict)
    return result_dict


def _create_uniform_known_format_timestamps_with_duplicates(n, format=FORMAT, duplicates=0):
    """
    Creates a list of n timestamps with a specified format
    :param n: Number of timestamps to create
    :param format: Timestamp string format. Defaults to ISO type with seconds spec.
    :return: List of timestamps
    """
    print('Creating test set...')
    i = 0
    if duplicates > 0:
        stop_index = int(n / duplicates)
    else:
        stop_index = n + 1
    timestamp = datetime(year=2000, month=1, day=1)
    list_of_timestamps = []
    while i < n:
        timestamp += timedelta(seconds=1)
        list_of_timestamps.append(timestamp.strftime(format))
        i += 1
        if i >= stop_index:
            to_repeat = list_of_timestamps.copy()
            for x in range(duplicates):
                list_of_timestamps.extend(to_repeat)
            break
    print('Completed.\n\n')
    return list_of_timestamps


if __name__ == '__main__':

    import seaborn as sns

    sns.set(font='Franklin Gothic Book',
            rc={
                'axes.axisbelow': False,
                'axes.edgecolor': 'lightgrey',
                'axes.facecolor': 'None',
                'axes.grid': False,
                'axes.labelcolor': 'black',
                'axes.spines.right': False,
                'axes.spines.top': False,
                'figure.facecolor': 'white',
                'lines.solid_capstyle': 'round',
                'patch.edgecolor': 'w',
                'patch.force_edgecolor': True,
                'text.color': 'black',
                'xtick.bottom': True,
                'xtick.color': 'grey',
                'xtick.direction': 'out',
                'xtick.top': False,
                'ytick.color': 'grey',
                'ytick.direction': 'out',
                'ytick.left': True,
                'ytick.right': False})
    sns.set_context("talk", rc={"font.size": 16,
                                "axes.titlesize": 20,
                                "axes.labelsize": 18})

    result_dict = trend_test(n=1000000, min_duplicates=0, max_duplicates=100, interval_value=20, trials=3)
    f = plt.figure()
    ax = f.add_subplot(1, 1, 1)
    for i in result_dict.keys():
        ax.plot(result_dict[i].keys(), result_dict[i].values())
    ax.legend(result_dict.keys(), frameon=False)
    ax.set_ylim(0, 3000)
    ax.set_ylabel('Average parsing time over 3 trials (ms)')
    ax.set_xlabel('Number of duplicates per timestamp string')
    ax.set_title('Parsing time of 1 million strings with timestamp format = {}'.format(FORMAT), pad=40)
    plt.show()

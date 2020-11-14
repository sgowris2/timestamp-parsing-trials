from datetime import datetime, timedelta
from test_runners import single_test_runner
from methods import *
import matplotlib.pyplot as plt

FORMAT = '%d-%m-%Y %H:%M:%S'
Y_LIMIT = 5000


def single_test(trials=3):
    ts_list = _create_uniform_known_format_timestamps(10000)

    # Test strptime
    print('Testing strptime...')
    single_test_runner(f=apply_strptime, data_list=ts_list, trials=trials, format=FORMAT)

    # Test pandas.to_datetime without infer
    print('Testing pandas.to_datetime without infer...')
    single_test_runner(f=apply_pd_to_datetime, data_list=ts_list, trials=trials)

    # Test pandas.to_datetime with infer
    print('Testing pandas.to_datetime with infer...')
    single_test_runner(f=apply_pd_to_datetime, data_list=ts_list, trials=trials, infer=True)

    # Test pandas.to_datetime with specified format
    print('Testing pandas.to_datetime with specified format...')
    single_test_runner(f=apply_pd_to_datetime, data_list=ts_list, trials=trials, format=FORMAT)


def trend_test(min_size=10000, max_size=1000000, interval_type='log', interval_value=1, trials=3):
    
    result_dict = {'time.strptime': dict(),
                   'pandas.to_datetime without infer': dict(),
                   'pandas.to_datetime with infer': dict(),
                   'pandas.to_datetime with specified format': dict(),
                   'pre-built lookup mapping': dict()}
    timing_dict = {'time.strptime': 0,
                   'pandas.to_datetime without infer': 0,
                   'pandas.to_datetime with infer': 0,
                   'pandas.to_datetime with specified format': 0,
                   'pre-built lookup mapping': 0}
    ts_list = _create_uniform_known_format_timestamps(max_size)

    dataset_size = min_size

    while dataset_size <= max_size:

        if timing_dict['time.strptime'] <= Y_LIMIT:
            print('\ntime.strptime')
            result_dict['time.strptime'][dataset_size] = single_test_runner(apply_strptime,
                                                                              data_list=ts_list[0:dataset_size],
                                                                              trials=trials,
                                                                              format=FORMAT)
            timing_dict['time.strptime'] = result_dict['time.strptime'][dataset_size]
        else:
            result_dict['time.strptime'][dataset_size] = None
            
        if timing_dict['pandas.to_datetime without infer'] <= Y_LIMIT:
            print('\npandas.to_datetime without infer')
            result_dict['pandas.to_datetime without infer'][dataset_size] = single_test_runner(
                apply_pd_to_datetime,
                trials=trials,
                data_list=ts_list[0:dataset_size])
            timing_dict['pandas.to_datetime without infer'] = \
                result_dict['pandas.to_datetime without infer'][dataset_size]
        else:
            result_dict['pandas.to_datetime without infer'][dataset_size] = None
        
        if timing_dict['pandas.to_datetime with infer'] <= Y_LIMIT:
            print('\npandas.to_datetime with infer')
            result_dict['pandas.to_datetime with infer'][dataset_size] = \
                single_test_runner(apply_pd_to_datetime,
                                   data_list=ts_list[0:dataset_size],
                                   trials=trials,
                                   infer=True)
            timing_dict['pandas.to_datetime with infer'] = \
                result_dict['pandas.to_datetime with infer'][dataset_size]
        else:
            result_dict['pandas.to_datetime with infer'][dataset_size] = None

        if timing_dict['pandas.to_datetime with specified format'] <= Y_LIMIT:
            print('\npandas.to_datetime with specified format')
            result_dict['pandas.to_datetime with specified format'][dataset_size] = \
                single_test_runner(
                    apply_pd_to_datetime,
                    data_list=ts_list[0:dataset_size],
                    trials=trials,
                    format=FORMAT)
            timing_dict['pandas.to_datetime with specified format'] = \
                result_dict['pandas.to_datetime with specified format'][dataset_size]
        else:
            result_dict['pandas.to_datetime with specified format'][dataset_size] = None

        if timing_dict['pre-built lookup mapping'] <= Y_LIMIT:
            print('\npre-built lookup mapping')
            result_dict['pre-built lookup mapping'][dataset_size] = \
                single_test_runner(
                    apply_prebuilt_memos,
                    data_list=pd.Series(ts_list[0:dataset_size]),
                    trials=trials,
                    format=FORMAT,
                    start_time=datetime(2000, 1, 1),
                    end_time=datetime(2000, 1, 1) + timedelta(minutes=dataset_size))
            timing_dict['pre-built lookup mapping'] = \
                result_dict['pre-built lookup mapping'][dataset_size]
        else:
            result_dict['pre-built lookup mapping'][dataset_size] = None

        if interval_type == 'log':
            dataset_size *= (2 ** interval_value)
        else:
            dataset_size += interval_value

    print(result_dict)
    return result_dict


def _create_uniform_known_format_timestamps(n, format=FORMAT):
    """
    Creates a list of n timestamps with a specified format
    :param n: Number of timestamps to create
    :param format: Timestamp string format. Defaults to ISO type with seconds spec.
    :return: List of timestamps
    """
    print('Creating test set...')
    i = 0
    timestamp = datetime(year=2000, month=1, day=1)
    list_of_timestamps = []
    while i < n:
        timestamp += timedelta(minutes=1)
        list_of_timestamps.append(timestamp.strftime(format))
        i += 1
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

    result_dict = trend_test(min_size=1024, max_size=1200000, trials=3)
    f = plt.figure()
    ax = f.add_subplot(1, 1, 1)
    for i in result_dict.keys():
        ax.plot(result_dict[i].keys(), result_dict[i].values())
        ax.set_xscale('log')
    ax.legend(result_dict.keys(), frameon=False)
    ax.set_ylim(0, Y_LIMIT)
    ax.set_ylabel('Average parsing time over 3 trials (ms)')
    ax.set_xlabel('Number of timestamp strings')
    ax.set_title('Parsing time with timestamp format = {}'.format(FORMAT), pad=40)
    plt.show()

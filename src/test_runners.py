from time import time


def single_test_runner(f, data_list, trials=3, **kwargs):
    total_time = 0

    for i in range(trials):
        start = time()
        f(data_list, **kwargs)
        end = time()
        total_time += (end - start)

    avg = round(1000 * total_time / float(trials), 3)
    per_timestamp_avg_us = round(1000000 * total_time / (len(data_list) * trials), 3)

    print('-------------------------------------------------'
          '\nNo. of trials: {}  |  '
          'Total time: {} ms  |  '
          'Avg per loop of {} timestamps: {} ms  |  '
          'Avg per timestamp: {} us\n'.format(trials,
                                              round(1000 * total_time, 3),
                                              len(data_list), avg,
                                              per_timestamp_avg_us))
    return avg

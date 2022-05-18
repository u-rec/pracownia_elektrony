import statistics

d_dist = 0.1


def average(data):
    n = len(data)
    av = sum(data) / n
    dev = (statistics.variance(data) / n) ** (1 / 2)
    if any(data > av * 1.5) or any(data < av / 2):
        raise Exception('probably wrong calculations!')
    return av, dev


def analyze_averages(data):
    data = sorted(data.items())
    l1, ((t1, dt1), (d1, dd1)) = data[0]
    l2, ((t2, dt2), (d2, dd2)) = data[1]

    distance = l2 - l1
    time = t2 - t1
    velocity = distance / time
    d_velocity = (distance + d_dist) / (time - dt2 - dt1) - velocity
    dx = velocity * (d2 ** 2 - d1 ** 2) ** (1 / 2)

    return (time, time ** (1 / 2)), (velocity, d_velocity), dx


def analyze_raw_data(data):
    result = {}
    for voltage, v_data in data.items():
        result[voltage] = {}
        for dist, d_data in v_data.items():
            big_time = [el[0] for el in d_data]
            small_time = [el[1] for el in d_data]
            result[voltage][dist] = (average(big_time), average(small_time))
    return result

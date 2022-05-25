import statistics

d_dist = 0.1


class RawResult:
    def __init__(self, val, dev):
        self.val = val
        self.d = dev


class Result:
    def __init__(self, t, v, dx):
        self.time = t
        self.time_sqrt = t ** (1 / 2)
        self.velocity = v
        self.diffusion = dx


def average(data):
    n = len(data)
    av = sum(data) / n
    dev = (statistics.variance(data) / n) ** (1 / 2)
    if any(data > av * 1.5) or any(data < av / 2):
        raise Exception('probably wrong calculations!')
    return RawResult(av, dev)


def analyze_averages(data):
    data = sorted(data.items())
    l1, (time1, diffus_t1) = data[0]
    l2, (time2, diffus_t2) = data[1]

    distance = l2 - l1
    time = time2.val - time1.val

    v = distance / time
    dv = ((d_dist / time) ** 2 + ((distance / (time ** 2)) ** 2) * (time1.d ** 2 + time2.d ** 2)) ** (1 / 2)
    velocity = RawResult(v, dv)

    sq_diff = (diffus_t2.val ** 2 - diffus_t1.val ** 2) ** (1 / 2)
    dx = velocity.val * sq_diff
    ddx2 = (sq_diff * velocity.d) ** 2 + \
           ((velocity.val / sq_diff) ** 2) * ((diffus_t1.val * diffus_t1.d) ** 2 + (diffus_t2.val * diffus_t2.d))
    diffusion = RawResult(dx, ddx2 ** (1 / 2))

    return Result(time, velocity, diffusion)


def analyze_raw_data(data):
    result = {}
    for voltage, v_data in data.items():
        result[voltage] = {}
        for dist, d_data in v_data.items():
            big_time = [el[0] for el in d_data]
            small_time = [el[1] for el in d_data]
            result[voltage][dist] = (average(big_time), average(small_time))
    return result

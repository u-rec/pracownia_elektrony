from load_file import get_next_file
from analyze import analyze_averages, analyze_raw_data, RawResult, Result
from resultbuilder import ResultBuilder


# © 2022 Jerzy Denisiewicz <j.denisiewicz@student.uw.edu.pl>


def collect_all_data():
    data = {}
    for file in get_next_file():
        if file.voltage not in data:
            data[file.voltage] = {}
        if file.distance not in data[file.voltage]:
            data[file.voltage][file.distance] = []
        data[file.voltage][file.distance].append(
            (file.plot_receiver.increase_value - file.plot_source.increase_value,
             file.plot_receiver.decrease_value - file.plot_receiver.increase_value))
        if file.plot_source.t_unit != '(us)' or file.plot_receiver.t_unit != '(us)':
            raise Exception
    return data


def main():
    data = collect_all_data()
    raw_result = ResultBuilder(
        ('voltage', 'distance', 'drift_time', 'd_drift_time', 'rec_time_diff', 'd_rec_time_diff')
    )
    developed_result = ResultBuilder(
        ('voltage', 't_drift', 'drift_velocity', 'd_drift_velocity', 'dx', 'd_dx', 'sqrt_t_drift')
    )
    for voltage, v_data in sorted(analyze_raw_data(data).items()):
        r = analyze_averages(v_data)
        developed_result.add(
            [str(val) for val in
             (voltage, r.time, r.velocity.val, r.velocity.d, r.diffusion.val, r.diffusion.d, r.time_sqrt)])
        for distance, (drift, diff) in v_data.items():
            raw_result.add(
                [str(val) for val in (voltage, distance, drift.val, drift.d, diff.val, diff.d)])
    raw_result.save('raw_data.txt')
    developed_result.save('results.txt')


if __name__ == '__main__':
    main()

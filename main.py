from load_file import get_next_file
from analyze import analyze_averages, analyze_raw_data
from resultbuilder import ResultBuilder

# © 2022 Jerzy Denisiewicz <j.denisiewicz@student.uw.edu.pl>


def collect_all_data():
    data = {}
    for distance, voltage, (plot_source, plot_receiver), name in get_next_file():
        if voltage not in data:
            data[voltage] = {}
        if distance not in data[voltage]:
            data[voltage][distance] = []
        data[voltage][distance].append((plot_receiver.increase_value - plot_source.increase_value,
                                        plot_receiver.decrease_value - plot_receiver.increase_value))
        if plot_source.t_unit != '(us)' or plot_receiver.t_unit != '(us)':
            raise Exception
    return data


def main():
    data = collect_all_data()
    raw_result = ResultBuilder(
        ('voltage', 'distance', 'drift_time', 'd_drift_time', 'rec_time_diff', 'd_rec_time_diff')
    )
    developed_result = ResultBuilder(
        ('voltage', 't_drift', 'drift_velocity', 'd_drift_velocity', 'dx', 'sqrt_t_drift')
    )
    for voltage, v_data in sorted(analyze_raw_data(data).items()):
        (t_drift, sqrt_t_drift), (drift_v, d_drift_v), dx = analyze_averages(v_data)
        developed_result.add([str(val) for val in (voltage, t_drift, drift_v, d_drift_v, dx, sqrt_t_drift)])
        for distance, ((drift, d_drift), (diff, d_diff)) in v_data.items():
            raw_result.add([str(val) for val in (voltage, distance, drift, d_drift, diff, d_diff)])
    raw_result.save('raw_data.txt')
    developed_result.save('results.txt')


if __name__ == '__main__':
    main()

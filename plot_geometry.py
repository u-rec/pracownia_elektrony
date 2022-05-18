from dataclasses import dataclass
import numpy as np
from scipy.optimize import curve_fit


class Plot:
    v_unit: str
    t_unit: str
    dt = np.dtype([('time', float), ('voltage', float)])

    def __init__(self, nparray, units, decrease=False):
        self.t_unit, self.v_unit = tuple(units)
        array_t = nparray.T
        self.line = None
        self.data = np.array(list(zip(array_t[0], array_t[1])), dtype=self.dt)
        self.sort_plot()
        self.max_index, self.max_val = self.find_max()
        self.average_noise = self.find_bg_noise()
        self.increase_value = self.get_time_of_first_peak(True)
        if decrease:
            self.decrease_value = self.get_time_of_first_peak(False)

    def sort_plot(self):
        np.sort(self.data, order='time')

    def find_max(self):
        index = np.argmax(self.data['voltage'])
        return index, self.data[index]

    def find_bg_noise(self):
        last_low = min(self.max_index, 200) -\
                    np.argmax(np.flip(self.data['voltage'][:self.max_index]) <
                              self.max_val['voltage'] / 20) + \
                    max(0, self.max_index - 200) - 20
        return np.mean(self.data['voltage'][max(0, last_low - 150):last_low])

    def find_first_above_half(self):
        return np.argmax(self.data['voltage'] > ((self.max_val['voltage'] + self.average_noise) / 2))

    def find_first_below_half(self):
        return np.argmax(self.data[self.max_index:]['voltage'] < ((self.max_val['voltage'] + self.average_noise) / 2)) \
                + self.max_index

    def fit_line(self, increase):
        if increase:
            index = self.find_first_above_half()
        else:
            index = self.find_first_below_half()
        self.line = Line.from_points(self.data[index - 3:index + 4])

    def get_time_of_first_peak(self, increase):
        self.fit_line(increase)
        return self.line.get_x_from_y((self.max_val['voltage'] + self.average_noise) / 2)


@dataclass
class Line:
    a: float
    b: float

    @classmethod
    def from_points(cls, points):
        x_data = points['time']
        y_data = points['voltage']
        popt, _ = curve_fit(lambda x, a, b: a * x + b, x_data, y_data)
        return cls(popt[0], popt[1])

    def get_x_from_y(self, y):
        if self.a == 0:
            return 0
        return (y - self.b) / self.a


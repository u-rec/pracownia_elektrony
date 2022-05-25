import os
from plot_geometry import Plot
import numpy as np

directory = '/home/jurek/Documents/Studia/VI/pracownia/elektrony/pomiary'


class Series:
    def __init__(self, dist, v, plots, file):
        self.distance = dist
        self.voltage = v
        self.plot_source = plots[0]
        self.plot_receiver = plots[1]
        self.file = file


def read_file(filename):
    f = open(filename, "r")
    lines = f.readlines()
    units1 = lines[1].strip().split('\t')[0:2]
    units2 = lines[1].strip().split('\t')[::2]
    first = True
    for line in lines[3:]:
        row = line.split('\t')
        time = float(row[0])
        vol1 = float(row[1])
        vol2 = float(row[2])
        if first:
            ar1 = np.array([[time, vol1]])
            ar2 = np.array([[time, vol2]])
            first = False
        else:
            ar1 = np.vstack((ar1, np.array([[time, vol1]])))
            ar2 = np.vstack((ar2, np.array([[time, vol2]])))
    return Plot(ar1, units1), Plot(ar2, units2, decrease=True)


def get_next_file():
    for filename in os.listdir(directory):
        if filename.endswith("png"):
            continue
        par = filename.split('_')
        if par[0] == '13':
            dist = 94.2
        elif par[0] == '23':
            dist = 48.2
        else:
            dist = 46.0
        voltage = int(par[1])
        new_dir = os.path.join(directory, filename)
        if os.path.isdir(new_dir):
            for file in os.listdir(new_dir):
                yield Series(dist, voltage, read_file(os.path.join(new_dir, file)), file)

import numpy as np
from matplotlib.figure import Figure as FIG
from matplotlib import pyplot as plt
import utils
from math_process import DiscreteFunction

from matplotlib import rcParams

rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['', 'Flexo', 'Microsoft Yahei UI Light', 'Tahoma']


class Measurement:
    class Data:

        def __init__(self, spl=0.0, phase=0.0):
            self.spl = spl
            self.phase = phase

    def __init__(self, measurement_content):
        self.original_content = measurement_content
        self._data_dict = {}
        self._freq_list = []
        for line in measurement_content:
            if '*' not in line:

                assert isinstance(line, str)
                split = line.split(',')

                # Measurement type
                if len(split) == 3:
                    freq, spl, phase = split
                    freq, spl, phase = float(freq), float(spl), float(phase)
                    self._data_dict[freq] = self.Data(spl=spl, phase=phase)
                    self._freq_list.append(freq)

                # Target Curve type
                if len(split) == 2:
                    freq, spl = split
                    freq, spl = float(freq), float(spl)
                    self._data_dict[freq] = self.Data(spl=spl, phase=0.0)
                    self._freq_list.append(freq)

    def data(self, freq):
        return self._data_dict[freq]

    def get_freq_list(self):
        return self._freq_list

    def get_spl_list(self):
        ret = []
        for freq in self.get_freq_list():
            ret.append(self.data(freq).spl)
        return ret


measure = Measurement(open('fr.txt'))
target = Measurement(open('target_rtings.txt'))

func_measure = DiscreteFunction(measure.get_freq_list(), measure.get_spl_list())
for x in range(10, 100):
    print(func_measure.get_y(x))

fig1, ax1 = plt.subplots()
assert isinstance(fig1, FIG)

fig1.set_size_inches(12, 6)
# fig1.set_size_inches(21.60,10.80)


ax1.semilogx(measure.get_freq_list(), measure.get_spl_list())
ax1.semilogx(target.get_freq_list(), target.get_spl_list())

ax1.set_xlim(10, 24000)

ax1.grid(axis='both', which='minor', c=utils.normalize_rgba((225, 225, 225, 255)))
ax1.grid(axis='both', which='major')

ax1.spines['right'].set_color(utils.normalize_rgba((225, 225, 225, 255)))
ax1.spines['top'].set_color(utils.normalize_rgba((225, 225, 225, 255)))

ax1.spines['bottom'].set_color(utils.normalize_rgba((5, 168, 241, 255)))
ax1.spines['bottom'].set_linewidth(1.5)

ax1.spines['left'].set_color(utils.normalize_rgba((249, 117, 144, 255)))
ax1.spines['left'].set_linewidth(1.5)


def formatter_freq(x, pos):
    if x >= 1000:
        formatted = '%1.1f' % (x / 1000)
        if not formatted == int(x / 1000):
            return str(int(x / 1000)) + "k"
        else:
            return str(formatted) + "k"
    return int(x)


formatter = plt.FuncFormatter(formatter_freq)
ax1.xaxis.set_major_formatter(formatter)
ax1.xaxis.set_minor_formatter(formatter)

for tick in ax1.xaxis.get_major_ticks():
    tick.label.set_fontsize(8)
    # tick.label.set_rotation('45')
    tick.label.set_color(utils.normalize_rgba((5, 168, 241, 255)))

for tick in ax1.xaxis.get_minor_ticks():
    tick.label.set_fontsize(7)
    # tick.label.set_rotation('45')

plt.xlabel("Frequency / Hz", fontsize=10)
plt.ylabel("SPL / dB", fontsize=10)

plt.show()

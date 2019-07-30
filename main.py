import numpy as np
from matplotlib.figure import Figure as FIG
from matplotlib import pyplot as plt
from matplotlib import rcParams

from math_process import *
from utils import *

rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['', 'Flexo', 'Microsoft Yahei UI Light', 'Tahoma']

measure = Measurement(open('fr.txt'))
target = Measurement(open('target_rtings.txt'))

func_measure = DiscreteFunction(measure.get_freq_list(), measure.get_spl_list(), definition=[20, 21000])
func_target = DiscreteFunction(target.get_freq_list(), target.get_spl_list(), definition=[20, 21000])

func_measure.add_bias(30.1)

fit = FuncFitting(func_target, func_measure)
print(func_measure.get_y(20))
fit.fit(500, [20, 21000])

if 0 == range(1):  # remember to del this line

    fig1, ax1 = plt.subplots()
    assert isinstance(fig1, FIG)

    fig1.set_size_inches(12, 6)
    # fig1.set_size_inches(21.60,10.80)

    ax1.semilogx(measure.get_freq_list(), measure.get_spl_list())
    ax1.semilogx(target.get_freq_list(), target.get_spl_list())

    ax1.set_xlim(10, 24000)

    ax1.grid(axis='both', which='minor', c=normalize_rgba((225, 225, 225, 255)))
    ax1.grid(axis='both', which='major')

    ax1.spines['right'].set_color(normalize_rgba((225, 225, 225, 255)))
    ax1.spines['top'].set_color(normalize_rgba((225, 225, 225, 255)))

    ax1.spines['bottom'].set_color(normalize_rgba((5, 168, 241, 255)))
    ax1.spines['bottom'].set_linewidth(1.5)

    ax1.spines['left'].set_color(normalize_rgba((249, 117, 144, 255)))
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
        tick.label.set_color(normalize_rgba((5, 168, 241, 255)))

    for tick in ax1.xaxis.get_minor_ticks():
        tick.label.set_fontsize(7)
        # tick.label.set_rotation('45')

    plt.xlabel("Frequency / Hz", fontsize=10)
    plt.ylabel("SPL / dB", fontsize=10)

    plt.show()

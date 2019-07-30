from matplotlib.figure import Figure as FIG
from matplotlib import pyplot as plt


def normalize_rgba(tup):
    return float(tup[0] / 255), float(tup[1] / 255), float(tup[2] / 255), float(tup[3] / 255)


class Drawing:

    @staticmethod
    def formatter_freq(x, pos):
        if x >= 1000:
            formatted = '%1.1f' % (x / 1000)
            if not formatted == int(x / 1000):
                return str(int(x / 1000)) + "k"
            else:
                return str(formatted) + "k"
        return int(x)

    def __init__(self):
        # plt.ion()
        self.fig1, self.ax1 = plt.subplots()
        self.ax1.set_xlim(20, 21000)

        self.ax1.grid(axis='both', which='minor', c=normalize_rgba((225, 225, 225, 255)))
        self.ax1.grid(axis='both', which='major')

        self.ax1.spines['right'].set_color(normalize_rgba((225, 225, 225, 255)))
        self.ax1.spines['top'].set_color(normalize_rgba((225, 225, 225, 255)))

        self.ax1.spines['bottom'].set_color(normalize_rgba((5, 168, 241, 255)))
        self.ax1.spines['bottom'].set_linewidth(1.5)

        self.ax1.spines['left'].set_color(normalize_rgba((249, 117, 144, 255)))
        self.ax1.spines['left'].set_linewidth(1.5)

        plt.xlabel("Frequency / Hz", fontsize=10)
        plt.ylabel("SPL / dB", fontsize=10)

        self.fig1.set_size_inches(12, 6)

    def draw_semi_log_x(self, x, y):

        self.ax1.semilogx(x, y)

        fmt = plt.FuncFormatter(Drawing.formatter_freq)
        self.ax1.xaxis.set_major_formatter(fmt)
        self.ax1.xaxis.set_minor_formatter(fmt)
        for tick in self.ax1.xaxis.get_major_ticks():
            tick.label.set_fontsize(8)
            # tick.label.set_rotation('45')
            tick.label.set_color(normalize_rgba((5, 168, 241, 255)))

        for tick in self.ax1.xaxis.get_minor_ticks():
            tick.label.set_fontsize(7)
            # tick.label.set_rotation('45')

    def show(self):
        plt.draw()
        plt.show()

    def get_plt(self):
        return plt


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

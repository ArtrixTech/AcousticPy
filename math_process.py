from utils import Drawing


class DiscreteFunction:

    def __init__(self, x_list, y_list, definition=None):

        assert isinstance(y_list, list) and isinstance(x_list, list)
        assert len(x_list) == len(y_list)
        self._original_x = x_list
        self._original_y = y_list
        if not definition:
            self.definition = [min(x_list), max(x_list)]
        else:
            if min(x_list) <= definition[0] and max(x_list) >= definition[1]:
                self.definition = definition
            else:
                raise ValueError("Input x value is not equal or bigger than definition. x is in " + str(
                    [min(x_list), max(x_list)]) + " and definition is " + str(definition))

    def _in_def(self, x):
        if self.definition[0] <= x <= self.definition[1]:
            return True
        return False

    def _min_dist_point(self, x):

        """
        :param x: input x value
        :return: x1, x2. These x-values are the nearest original-x value.
        """
        for index in range(len(self._original_x) - 1):
            if self._original_x[index] <= x <= self._original_x[index + 1]:
                mid_index = index
                return self._original_x[mid_index], self._original_x[mid_index + 1]

    def _min_dist_point_continuous(self, x, start_index=0):
        """
        :param x: input x value
        :param start_index: searching start index
        :return: x1, x2. These x-values are the nearest original-x value.
        """

        for index in range(start_index, len(self._original_x) - 1):
            if self._original_x[index] <= x <= self._original_x[index + 1]:
                mid_index = index
                return self._original_x[mid_index], self._original_x[mid_index + 1], mid_index

    def _get_origin_y_by_x(self, x):
        assert isinstance(self._original_x, list)
        index = self._original_x.index(x)
        return self._original_y[index]

    def get_y(self, x):
        if self._in_def(x):

            x_l, x_r = self._min_dist_point(x)
            y_l, y_r = self._get_origin_y_by_x(x_l), self._get_origin_y_by_x(x_r)

            dist_l, dist_r = abs(x - x_l), abs(x - x_r)
            delta_y = y_r - y_l

            return dist_l / (dist_l + dist_r) * delta_y + y_l
        else:
            raise ValueError("Input x value is not in the definition range.")

    def _get_y_continuous(self, x, last_index):
        if self._in_def(x):

            x_l, x_r, new_index = self._min_dist_point_continuous(x, last_index)

            y_l, y_r = self._get_origin_y_by_x(x_l), self._get_origin_y_by_x(x_r)

            dist_l, dist_r = abs(x - x_l), abs(x - x_r)
            delta_y = y_r - y_l

            return dist_l / (dist_l + dist_r) * delta_y + y_l, new_index
        else:
            raise ValueError("Input x value is not in the definition range.")

    def add_bias(self, bias):
        for i in range(len(self._original_y)):
            self._original_y[i] += bias

    def clone(self):
        return DiscreteFunction(self._original_x, self._original_y, self.definition)

    def definition_range_length(self):
        return self.definition[1] - self.definition[0]

    def sample_x(self, sample_rate, sample_range=None, low_freq_gain=True):
        if not sample_range:
            sample_range = self.definition
        if not low_freq_gain:
            interval = (sample_range[1] - sample_range[0]) / sample_rate
            rt = []
            for tick in range(sample_rate):
                res = sample_range[0] + tick * interval
                rt.append(res)
            return rt
        else:
            # Low frequency range always are sparse in the figure, as this low_freq_gain is to add more samples here.
            low_freq_range = [sample_range[0], 100]
            low_freq_gain_k = 64

            low_freq_range_length = 100 - sample_range[0]
            sample_range_length = sample_range[1] - sample_range[0]

            low_freq_proportion = low_freq_range_length / sample_range_length
            low_freq_sample_rate = int(low_freq_proportion * sample_rate * low_freq_gain_k)

            low_freq = self.sample_x(low_freq_sample_rate, low_freq_range, low_freq_gain=False)
            other_freq = self.sample_x(sample_rate, [low_freq_range[1], sample_range[1]], low_freq_gain=False)
            return low_freq + other_freq

    def sample_y(self, sample_rate, def_range=None):
        x_list = self.sample_x(sample_rate, def_range)
        rt = []
        last_index = 0
        for x in x_list:
            res, last_index = self._get_y_continuous(x, last_index)
            rt.append(res)
        return rt


class FuncFitting:
    def __init__(self, target_func, input_func):
        assert isinstance(target_func, DiscreteFunction) and isinstance(input_func, DiscreteFunction)
        self.target_func = target_func.clone()
        self.input_func = input_func.clone()
        self.def_range = None

    @staticmethod
    def _get_diff(target_y, input_y):
        assert isinstance(target_y, list) and isinstance(input_y, list)
        assert len(target_y) == len(input_y)

        diff = 0
        for index in range(len(target_y)):
            diff += abs(target_y[index] - input_y[index])
        return diff

    def fit(self, sample_rate, def_range=None):
        if not def_range:
            if self.target_func.definition == self.input_func.definition:
                self.def_range = self.target_func.definition
            else:
                raise ValueError("Definition range not consistent. Try input a specific range.")
        else:
            self.def_range = def_range

        drawing = Drawing()
        plt = drawing.get_plt()
        plt.ion()

        target_y_list = self.target_func.sample_y(sample_rate, def_range)
        drawing.draw_semi_log_x(self.target_func.sample_x(sample_rate, def_range), target_y_list)

        for bias in range(200):
            self.input_func.add_bias(0.01)

            input_y_list = self.input_func.sample_y(sample_rate, def_range)
            drawing.draw_semi_log_x(self.input_func.sample_x(sample_rate, def_range), input_y_list)

            print("drawn:bias=" + str(bias*0.01) + ", diff=" + str(self._get_diff(target_y_list, input_y_list)))
            plt.pause(0.01)
            # drawing.show()

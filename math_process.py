class DiscreteFunction:

    def __init__(self, x_list, y_list, definition=None):

        assert len(x_list) == len(y_list)
        self._original_x = x_list
        self._original_y = y_list
        if not definition:
            self.definition = [min(x_list), max(x_list)]

    def _in_def(self, x):
        if self.definition[0] <= x <= self.definition[1]:
            return True
        return False

    def _min_dist_point(self, x):

        """
        :param x: input x value
        :return: list, consist of 2 value: x1, x2. These x-values are the nearest original-x data.
        """

        mid_index = 0
        for index in range(len(self._original_x) - 1):
            if self._original_x[index] <= x <= self._original_x[index + 1]:
                mid_index = index

        return self._original_x[mid_index], self._original_x[mid_index + 1]

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

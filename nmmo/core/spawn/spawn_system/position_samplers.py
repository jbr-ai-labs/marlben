import numpy as np
from .base_samplers import UniformSampler, RangeSampler, ListSampler, ConstantSampler, ChoiceSampler


class PositionSampler:
    def __init__(self):
        pass

    def get_next(self):
        pass

    def reset(self, config):
        pass


class ConcurrentPositionSampler(PositionSampler):
    def __init__(self):
        super().__init__()
        self.x_sampler = None
        self.y_sampler = None

    def get_next(self):
        return self.x_sampler.get_next(), self.y_sampler.get_next()

    def reset(self, config):
        if self.x_sampler is None:
            map_height = config.MAP_HEIGHT
            map_width = config.MAP_WIDTH
            top, left = config.TOP_LEFT_CORNER

            horizontal_range = np.arange(left + 2, left + map_width, 4).tolist()
            vertical_range = np.arange(top + 2, top + map_height, 4).tolist()

            lefts = (left + np.zeros(len(vertical_range), dtype=np.int)).tolist()
            rights = ((left + map_width) + np.zeros(len(vertical_range), dtype=np.int)).tolist()
            highs = (top + np.zeros(len(horizontal_range), dtype=np.int)).tolist()
            lows = ((top + map_height) + np.zeros(len(horizontal_range), dtype=np.int)).tolist()

            border_x = horizontal_range + lefts + horizontal_range + rights
            border_y = lows + vertical_range + highs + vertical_range
            self.x_sampler = ListSampler(border_x)
            self.y_sampler = ListSampler(border_y)
        else:
            self.x_sampler.reset()
            self.y_sampler.reset()


class ContinuousPositionSampler(PositionSampler):
    def __init__(self):
        super().__init__()
        self.x_border_choice = None
        self.y_border_choice = None
        self.x_range_sampler = None
        self.y_range_sampler = None

    def get_next(self):
        if np.random.rand() < 0.5:
            return self.x_border_choice.get_next(), self.y_range_sampler.get_next()
        else:
            return self.x_range_sampler.get_next(), self.y_border_choice.get_next()

    def reset(self, config):
        if self.x_border_choice is None:
            map_height = config.MAP_HEIGHT
            map_width = config.MAP_WIDTH
            top, left = config.TOP_LEFT_CORNER
            self.x_border_choice = ChoiceSampler([left, left + map_width])
            self.y_border_choice = ChoiceSampler([top, top + map_height])
            self.x_range_sampler = UniformSampler(left, left + map_width)
            self.y_range_sampler = UniformSampler(top, top + map_height)


class UniformPositionSampler(PositionSampler):
    def __init__(self):
        super().__init__()
        self.x_sampler = None
        self.y_sampler = None

    def reset(self, config):
        map_height = config.MAP_HEIGHT
        map_width = config.MAP_WIDTH
        top, left = config.TOP_LEFT_CORNER
        self.x_sampler = UniformSampler(left, left + map_width)
        self.y_sampler = UniformSampler(top, top + map_height)

    def get_next(self):
        return self.x_sampler.get_next(), self.y_sampler.get_next()


class RangePositionSampler(PositionSampler):
    def __init__(self, r_range, c_range):
        super().__init__()
        self.x_sampler = None
        self.y_sampler = None
        self.r_range = r_range
        self.c_range = c_range

    def get_next(self):
        return self.x_sampler.get_next(), self.y_sampler.get_next()

    def reset(self, config):
        if self.x_sampler is None:
            map_height = config.MAP_HEIGHT
            map_width = config.MAP_WIDTH
            top, left = config.TOP_LEFT_CORNER

            r_range = [r + top for r in self.r_range]
            c_range = [c + left for c in self.c_range]

            self.x_sampler = ChoiceSampler(r_range)
            self.y_sampler = ChoiceSampler(c_range)

class MultiRangePositionSampler(PositionSampler):
    def __init__(self, r_ranges, c_ranges):
        super().__init__()
        self.x_samplers = None
        self.y_samplers = None
        self.r_ranges = r_ranges
        self.c_ranges = c_ranges
        self.num_ents = len(self.r_ranges)
        self.idx = 0

    def get_next(self):
        r = self.y_samplers[self.idx].get_next()
        c = self.x_samplers[self.idx].get_next()
        self.idx = (self.idx + 1) % self.num_ents
        return r, c

    def reset(self, config):
        if self.x_samplers is None:
            self.x_samplers = []
            self.y_samplers = []
            map_height = config.MAP_HEIGHT
            map_width = config.MAP_WIDTH
            top, left = config.TOP_LEFT_CORNER

            for range_num in range(len(self.r_ranges)):
                r_range = self.r_ranges[range_num]
                c_range = self.c_ranges[range_num]

                r_range = [r + top for r in r_range]
                c_range = [c + left for c in c_range]

                self.x_samplers.append(UniformSampler(*c_range))
                self.y_samplers.append(UniformSampler(*r_range))
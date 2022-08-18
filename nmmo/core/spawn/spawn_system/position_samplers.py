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
    def __init__(self, r_range=None, c_range=None):
        super().__init__()
        self.x_sampler = None
        self.y_sampler = None
        self.r_range = r_range
        self.c_range = c_range

    def reset(self, config):
        map_height = config.MAP_HEIGHT
        map_width = config.MAP_WIDTH
        top, left = config.TOP_LEFT_CORNER

        if self.r_range is None:
            r_start, r_end = top, top + map_height
        else:
            r_start, r_end = [r + top for r in self.r_range]
        
        if self.c_range is None:
            c_start, c_end = left, left + map_width
        else:
            c_start, c_end = [c + left for c in self.c_range]
        
        self.x_sampler = UniformSampler(r_start, r_end)
        self.y_sampler = UniformSampler(c_start, c_end)

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

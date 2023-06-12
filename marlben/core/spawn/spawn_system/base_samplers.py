import numpy as np


class Sampler:
    def get_next(self):
        pass

    def reset(self):
        pass


class ConstantSampler(Sampler):
    def __init__(self, c):
        self.c = c

    def get_next(self):
        return self.c


class RangeSampler(Sampler):
    def __init__(self, a, b):
        self.i = 0
        self.a = a
        self.b = b

    def get_next(self):
        x = self.a + (self.b - self.a) * self.i / abs(self.b - self.a)
        self.i = (self.i + 1) % (abs(self.b - self.a) + 1)
        return x

    def reset(self):
        self.i = 0


class UniformSampler(Sampler):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def get_next(self):
        return np.random.randint(self.a, self.b+1)


class ListSampler(Sampler):
    def __init__(self, list):
        self.list = list
        self.i = 0

    def get_next(self):
        x = self.list[self.i]
        self.i = (self.i + 1) % len(self.list)
        return x

    def reset(self):
        self.i = 0


class ChoiceSampler(Sampler):
    def __init__(self, list):
        self.list = list

    def get_next(self):
        return np.random.choice(self.list)

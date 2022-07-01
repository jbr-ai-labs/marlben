from nmmo.lib import utils


class SequentialLoader:
    '''config.AGENT_LOADER that spreads out agent populations'''

    def __init__(self, config):
        items = config.AGENTS
        for idx, itm in enumerate(items):
            itm.policyID = idx

        self.items = items
        self.idx = -1

    def __iter__(self):
        return self

    def __next__(self):
        self.idx = (self.idx + 1) % len(self.items)
        return self.idx, self.items[self.idx]


class Template(metaclass=utils.StaticIterable):
    def __init__(self):
        self.data = {}
        cls = type(self)

        # Set defaults from static properties
        for k, v in cls:
            self.set(k, v)

    def override(self, **kwargs):
        for k, v in kwargs.items():
            err = 'CLI argument: {} is not a Config property'.format(k)
            assert hasattr(self, k), err
            self.set(k, v)

    def set(self, k, v):
        if type(v) is not property:
            try:
                setattr(self, k, v)
            except:
                print('Cannot set attribute: {} to {}'.format(k, v))
                quit()
        self.data[k] = v

    def print(self):
        keyLen = 0
        for k in self.data.keys():
            keyLen = max(keyLen, len(k))

        print('Configuration')
        for k, v in self.data.items():
            print('   {:{}s}: {}'.format(k, keyLen, v))
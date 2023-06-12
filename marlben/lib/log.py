from collections import defaultdict


class Quill:
    def __init__(self):
        self.blobs = defaultdict(Blob)
        self.stats = defaultdict(list)

    def stat(self, key, val):
        self.stats[key].append(val)

    def register(self, key, tick):
        if key in self.blobs:
            blob = self.blobs[key]
        else:
            blob = Blob()
            self.blobs[key] = blob

        blob.tick = tick
        return blob

    @property
    def packet(self):
        logs = {key: blob.packet for key, blob in self.blobs.items()}
        return {'Log': logs, 'Stats': self.stats}


class Blob:
    def __init__(self):
        self.tracks = defaultdict(Track)

    def log(self, value, key=None):
        self.tracks[key].update(self.tick, value)

    @property
    def packet(self):
        return {key: track.packet for key, track in self.tracks.items()}

# Static blob analytics


class Track:
    def __init__(self):
        self.data = defaultdict(list)

    def update(self, tick, value):
        if type(value) != list:
            value = [value]

        self.data[tick] += value

    @property
    def packet(self):
        return self.data

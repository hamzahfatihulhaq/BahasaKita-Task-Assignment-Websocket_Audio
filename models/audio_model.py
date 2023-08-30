class Audio:
    def __init__(self, name, size, sample_rate, bit_depth, duration, file_type):
        self.name = name
        self.size = size
        self.sample_rate = sample_rate
        self.bit_depth = bit_depth
        self.duration = duration
        self.file_type = file_type

    def to_dict(self):
        return {
            "name": self.name,
            "size": self.size,
            "sample_rate": self.sample_rate,
            "bit_depth": self.bit_depth,
            "duration": self.duration,
            "file_type": self.file_type
        }



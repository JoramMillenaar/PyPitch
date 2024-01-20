import numpy as np


class AudioOverlapProcessor:
    def __init__(self, output_chunk_size, sample_rate):
        self.sample_rate = sample_rate
        self.output_chunk_size = output_chunk_size

        self.overlap_factor = None
        self.overlap_size = None
        self.buffer = None
        self.chunk_size = None

    def prime(self, chunk_size):
        self.overlap_factor = self.output_chunk_size // chunk_size
        self.overlap_size = int(chunk_size * self.overlap_factor)
        self.buffer = np.zeros(self.overlap_size, dtype=np.float32)
        self.chunk_size = self.overlap_size + chunk_size

    def process(self, audio_chunk):
        if self.buffer is None:
            self.prime(len(audio_chunk))
        chunk = np.concatenate((self.buffer, audio_chunk))
        self.buffer = chunk[-self.overlap_size:]
        return chunk

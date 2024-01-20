from typing import Protocol

import numpy as np
from numpy._typing import NDArray

from pypitch.fft import FFTAnalyser
from pypitch.services import base_frequency_indexes, loudest_harmonic_of_loudest_base
from pypitch.yin import yin_pitch_detection


class PitchDetector(Protocol):
    def detect_frequency(self, audio_chunk: NDArray) -> float:
        pass


class YinPitchDetector(PitchDetector):
    def __init__(self, sample_rate, threshold=0.1):
        self.sample_rate = sample_rate
        self.threshold = threshold

    def detect_frequency(self, audio_chunk: NDArray) -> float:
        frequency = yin_pitch_detection(audio_chunk, self.sample_rate, self.threshold)
        return frequency or 0


class AutoCorrelationPitchDetector(PitchDetector):
    def __init__(self, sample_rate, max_frequency=1000, min_frequency=80):
        self.sample_rate = sample_rate
        self.max_lag = int(sample_rate / min_frequency)
        self.min_lag = int(sample_rate / max_frequency)

    def detect_frequency(self, audio_chunk: NDArray) -> float:
        chunk_normalized = audio_chunk - np.mean(audio_chunk)

        corr = np.correlate(chunk_normalized, chunk_normalized, mode='full')
        corr_half = corr[corr.size // 2:]

        if self.min_lag >= self.max_lag or len(corr_half[self.min_lag:self.max_lag]) == 0:
            return 0

        peak_index = np.argmax(corr_half[self.min_lag:self.max_lag]) + self.min_lag
        return self.sample_rate / peak_index if peak_index != 0 else 0


class FFTPitchDetector(PitchDetector):
    def __init__(self, sample_rate: int, frequency_resolution: int = 3):
        self.fft = FFTAnalyser(sample_rate, frequency_resolution)

    def detect_frequency(self, audio_chunk: NDArray) -> float:
        fft_analytics = self.fft.analyse(audio_chunk)
        index_loudest = np.argmax(fft_analytics.magnitudes)
        return fft_analytics.frequency_range[index_loudest]


class HarmonicFFTPitchDetector(PitchDetector):
    def __init__(self, sample_rate, lenience: float = 1, frequency_resolution: int = 3):
        self.lenience = lenience
        self._cached_indexes = None
        self.fft = FFTAnalyser(sample_rate, frequency_resolution)

    def harmonic_indexes(self, frequencies):
        if self._cached_indexes is None:
            self._cached_indexes = base_frequency_indexes(frequencies, self.lenience)
        return self._cached_indexes

    def detect_frequency(self, audio_chunk: NDArray) -> float:
        fft_analytics = self.fft.analyse(audio_chunk)
        indexes = self.harmonic_indexes(fft_analytics.frequency_range)
        index = loudest_harmonic_of_loudest_base(indexes, fft_analytics.magnitudes)
        return fft_analytics.frequency_range[index]

import numpy as np


def base_frequency_indexes(frequencies: np.ndarray, lenience: float = 0.0):
    base_indices = [None] * len(frequencies)

    for i, freq in enumerate(frequencies):
        for j in range(i):
            base_freq = frequencies[j]
            if base_freq <= freq / 2:
                if abs(freq - (base_freq * round(freq / base_freq))) <= lenience:
                    base_indices[i] = j
                    break

    return base_indices


def loudest_harmonic_of_loudest_base(base_indices, magnitudes):
    harmonic_sums = {}
    loudest_harmonics = {}

    for i, base_index in enumerate(base_indices):
        if base_index is not None:
            harmonic_sums.setdefault(base_index, 0)
            harmonic_sums[base_index] += magnitudes[i]

            if base_index not in loudest_harmonics or magnitudes[i] > magnitudes[loudest_harmonics[base_index]]:
                loudest_harmonics[base_index] = i

    if not harmonic_sums:
        return None

    loudest_base_index = max(harmonic_sums, key=harmonic_sums.get)
    return loudest_harmonics[loudest_base_index]

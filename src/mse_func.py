import numpy as np


def calculate_mse(original, result):
    return ((original.astype(np.float64) - result.astype(np.float64)) ** 2).mean()

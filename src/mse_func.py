import numpy as np
from seam_carving import resize_image


def calculate_mse(original, result):
    if original.shape != result.shape:
        # using seam carving to handle different ratios
        if original.shape[0] > result.shape[0]:
            original = resize_image(original, result.shape[0], result.shape[1])
        else:
            result = resize_image(result, original.shape[0], original.shape[1])

    return ((original.astype(np.float64) - result.astype(np.float64)) ** 2).mean()

import numpy as np
from seam_carving import resize_image


def calculate_mse(original, result):
    M, N, C = original.shape
    temp = np.zeros((M, N, 3))
    if C == 4:
        for i in range(M):
            for j in range(N):
                if original[i, j, 3] == 0:
                    temp[i, j] = np.array([255, 255, 255])
                else:
                    temp[i, j] = original[i, j, :3]
    else:
        temp = original

    if temp.shape != result.shape:
        # using seam carving to handle different ratios
        if temp.shape[0] > result.shape[0]:
            temp = resize_image(temp, result.shape[0], result.shape[1])
        else:
            result = resize_image(result, temp.shape[0], temp.shape[1])

    return ((temp.astype(np.float64) - result.astype(np.float64)) ** 2).mean()

# This Module is for smoothing the zigzag points
import numpy as np
from scipy.interpolate import splprep, splev


def smooth_zigzag_points(zigzag_points, smoothness=0.5):
    x = [point[0] for point in zigzag_points]
    y = [point[1] for point in zigzag_points]

    tck, u = splprep([x, y], s=smoothness)
    
    u_new = np.linspace(u.min(), u.max(), len(zigzag_points) * 10)

    x_smooth, y_smooth = splev(u_new, tck)

    smooth_points = [(x, y) for x, y in zip(x_smooth, y_smooth)]

    return smooth_points


if __name__ == "__main__":
    zigzag_points = [
        (0, 0),
        (1, 0),
        (1, 1),
        (1, 2),
        (2, 2),
        (2, 3),
        (3, 3),
        (3, 4),
        (4, 4),
    ]

    smooth_points = smooth_zigzag_points(
        zigzag_points=zigzag_points,
        smoothness=0.5,
    )

    print(smooth_points)

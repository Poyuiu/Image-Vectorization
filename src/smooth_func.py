# This Module is for smoothing the zigzag points
import numpy as np
from scipy.interpolate import splprep, splev


def curve_fitting(zigzag_points, smoothness=0.5):
    """
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.splprep.html
    """
    x = [point[0] for point in zigzag_points]
    y = [point[1] for point in zigzag_points]

    tck, u = splprep([x, y], s=smoothness)

    u_new = np.linspace(u.min(), u.max(), len(zigzag_points) * 30)

    x_smooth, y_smooth = splev(u_new, tck)

    smooth_points = [(x, y) for x, y in zip(x_smooth, y_smooth)]

    return smooth_points


def mean_filter(zigzag_points, window_size=3):
    """Just mean the neighbors points."""
    smoothed_points = []

    for i in range(len(zigzag_points)):
        start = max(0, i - window_size // 2)
        end = min(i + window_size // 2 + 1, len(zigzag_points))

        neighbors = zigzag_points[start:end]
        avg_x = sum(point[0] for point in neighbors) / len(neighbors)
        avg_y = sum(point[1] for point in neighbors) / len(neighbors)

        smoothed_points.append((avg_x, avg_y))

    return smoothed_points


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

    smooth_points = mean_filter(
        zigzag_points=zigzag_points,
        window_size=3,
    )

    print(smooth_points, len(smooth_points))

    smooth_points = curve_fitting(
        zigzag_points=zigzag_points,
        smoothness=0.5,
    )

    print(smooth_points, len(smooth_points))

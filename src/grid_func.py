import cv2
import math
import copy
import numpy as np
import matplotlib.pyplot as plt
from io import StringIO
import smooth_func


def dist(color1, color2):
    # return sum((color1 - color2) ** 2) ** 0.5  # Euclidean distance
    return sum(np.abs(color1 - color2))


def get_piece_color_from_same_color_grid(image, M, N, start_i, start_j, visited):
    # some consts
    DIRECTION = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    CORNERS = [(0, 0), (0, 1), (1, 0), (1, 1)]

    visited[start_i][start_j] = True
    cur_color = tuple(image[start_i, start_j])

    # Python >= 3.8 would maintain the order of the set
    pieces = set()
    queue = [(start_i, start_j)]
    while queue:
        cur_point = queue.pop(0)

        for dx, dy in CORNERS:
            corner_point = (cur_point[0] + dx, cur_point[1] + dy)
            # Can svg use the points out of bound?
            # if corner_point[0] < M and corner_point[1] < N:
            pieces.add(corner_point)

        for dx, dy in DIRECTION:
            next_point = (cur_point[0] + dx, cur_point[1] + dy)
            if (
                next_point[0] < 0
                or next_point[0] >= M
                or next_point[1] < 0
                or next_point[1] >= N
                or visited[next_point[0]][next_point[1]]
                # allow a threshold
                # or dist(image[cur_point], image[next_point]) > 40
                # strict
                or not math.isclose(dist(image[cur_point], image[next_point]), 0.0)
            ):
                continue
            visited[next_point[0]][next_point[1]] = True
            queue.append(next_point)

    return list(pieces), cur_color


def get_same_color_regions(image, M, N):
    visited = [[False] * N for _ in range(M)]
    regions = []

    for i in range(M):
        for j in range(N):
            if not visited[i][j]:
                # get same color grid by BFS
                regions.append(
                    get_piece_color_from_same_color_grid(image, M, N, i, j, visited)
                )
    return regions

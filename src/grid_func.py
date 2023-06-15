import math
import numpy as np
import copy


def dist(color1, color2):
    # return sum((color1 - color2) ** 2) ** 0.5  # Euclidean distance
    return sum(np.abs(color1 - color2))


def get_region_area(piece):
    edge_points = np.array(list(copy.deepcopy(piece)))
    min_x, min_y = np.min(edge_points, axis=0)
    max_x, max_y = np.max(edge_points, axis=0)
    point_on_xy = np.zeros((max_x - min_x + 1, max_y - min_y + 1))

    for x, y in piece:
        point_on_xy[x - min_x, y - min_y] = 1

    area = 0
    for row in point_on_xy:
        first_one = np.where(row == 1)[0][0]
        last_one = np.where(row == 1)[0][-1]
        area = area + last_one - first_one + 1

    return area


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
    area = get_region_area(list(pieces))
    return list(pieces), cur_color, area


def get_same_color_regions(image, M, N):
    visited = [[False] * N for _ in range(M)]
    regions = []

    # clear out transparent background
    """
    if image.shape[2] == 4:
        for i in range(M):
            for j in range(N):
                if image[i,j,3] < 5:
                    visited[i][j] = True
    """

    for i in range(M):
        for j in range(N):
            if not visited[i][j]:
                # get same color grid by BFS
                r = get_piece_color_from_same_color_grid(image, M, N, i, j, visited)
                regions.append(r)
    return regions

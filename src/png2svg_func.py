import cv2
import copy
from io import StringIO
import smooth_func
import grid_func
import matplotlib.pyplot as plt
import k_means
import numpy as np


# debug用
def preview_piece(piece):
    x_coords = [coord[0] for coord in piece]
    y_coords = [coord[1] for coord in piece]

    plt.scatter(x_coords, y_coords)

    min_x = min(x_coords) - 1
    max_x = max(x_coords) + 1
    min_y = min(y_coords) - 1
    max_y = max(y_coords) + 1
    plt.xlim(min_x, max_x)
    plt.ylim(min_y, max_y)

    plt.show()


# debug用
def preview_images(image):
    plt.imshow(image)
    plt.show()


def svg_header(height, width):
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
        '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"\n'
        '"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n'
        f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg" version="1.1">\n'
    )


"""
def get_closed_path(edge_points):
    dir = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
    cur = edge_points.pop(0)
    ans = [cur]
    last_dir = 0

    while edge_points:
        for i in range(8):
            dx, dy = dir[(last_dir + i) % 8]
            if (cur[0] + dx, cur[1] + dy) in edge_points:
                cur = (cur[0] + dx, cur[1] + dy)
                last_dir = (last_dir + i + 4) % 8
                edge_points.remove(cur)
                ans.append(cur)
                break
        else:
            break

    return ans
"""


def get_close_edge_points(piece):
    edge_points = np.array(list(copy.deepcopy(piece)))
    min_x, min_y = np.min(edge_points, axis=0)
    max_x, max_y = np.max(edge_points, axis=0)
    # +1最大最小值都是包含
    # +2最外側保留一圈，後續使用要+1
    point_on_xy = np.zeros((max_x - min_x + 1 + 2, max_y - min_y + 1 + 2))

    for x, y in piece:
        point_on_xy[x - min_x + 1, y - min_y + 1] = 1
    # 找到圖內某個點
    cur = piece[0]
    cur = (max_x, cur[1])
    # 走到最右邊，當作close path的起點
    while point_on_xy[cur[0] - min_x + 1, cur[1] - min_y + 1] == 0:
        cur = (cur[0] - 1, cur[1])
    start_pos = cur
    ans = [start_pos]

    # 八個方向，依照逆時鐘順序
    dir = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
    # 由於最開始一直往右走，dir[0]的方向一定不是邊的位置
    last_dir = 0

    # 重複找下一個點，直到回歸起點
    while True:
        for i in range(8):
            dx, dy = dir[(last_dir + i) % 8]
            # 如果在邊上
            if point_on_xy[cur[0] + dx - min_x + 1, cur[1] + dy - min_y + 1] == 1:
                # 移動到下個點
                cur = (cur[0] + dx, cur[1] + dy)
                # 前一個點的方向，+1確保下次開始尋找的起點不是邊
                last_dir = (last_dir + i + 1 + 4) % 8
                ans.append(cur)
                break
        if cur == start_pos:
            break

    return ans


def write_svg_path(s, piece, color, smooth_type=1):
    # not drawing small groups, will show the background color
    # if len(piece) < 10: continue
    l = len(piece)
    # preview_piece(piece)
    edge_points = get_close_edge_points(piece)
    # preview_piece(edge_points)
    # edge_points = get_closed_path(edge_points)

    if smooth_type == 0:
        edge_points = edge_points
    elif smooth_type == 1:
        edge_points = smooth_func.mean_filter(edge_points)
    else:
        edge_points = smooth_func.curve_fitting(edge_points)

    s.write('<path d="')
    start = edge_points.pop(0)
    s.write(f"M {start[1]} {start[0]} ")
    for p in edge_points:
        s.write(f"L {p[1]} {p[0]} ")
    s.write(f'Z" stroke="none" fill="rgb({color[2]},{color[1]},{color[0]})" />\n')


def smooth_detail(img):
    height, width, _ = img.shape

    for i in range(1, height - 1):
        for j in range(1, width - 1):
            region = img[i - 1 : i + 2, j - 1 : j + 2, :]
            region = np.reshape(region, (-1, 3))

            count = np.sum((region == img[i, j]).all(axis=1))
            if count > 3:
                continue

            max = -1
            for c in region:
                count = np.sum((region == c).all(axis=1))
                if max < count:
                    max = count
                    max_color = c
                    if max >= 5:
                        break
            img[i, j] = max_color

    return img


def png2svg(image, sm):
    M, N, _ = image.shape
    s = StringIO()
    s.write(svg_header(M, N))

    # collect contiguous pixel groups by traversing image
    regions = grid_func.get_same_color_regions(image, M, N)

    regions = sorted(regions, key=lambda x: x[2], reverse=True)

    for piece, color, area in regions:
        write_svg_path(s, piece, color, smooth_type=sm)

    s.write("</svg>\n")
    return s.getvalue()


if __name__ == "__main__":
    # Warning: notice the image path (check your workspace directory)
    img = cv2.imread("flower.jpg")

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    print("Doing K means clustering")
    img = k_means.coverting_img(img, 32)
    # preview_images(img)

    print("Removing detail...")
    img = smooth_detail(img)
    # preview_images(img)

    img = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_RGB2BGR)

    print("Converting to svg file")
    svg_image = png2svg(img, 1)

    with open("result.svg", "w") as fh:
        fh.write(svg_image)

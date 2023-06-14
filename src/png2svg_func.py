import cv2
import copy
from io import StringIO
import smooth_func
import grid_func


def svg_header(height, width):
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
        '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"\n'
        '"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n'
        f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg" version="1.1">\n'
    )


def get_closed_path(edge_points):
    dir = [(1, 0), (0, 1), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    cur = edge_points.pop(0)
    ans = [cur]

    while edge_points:
        for dx, dy in dir:
            if (cur[0] + dx, cur[1] + dy) in edge_points:
                cur = (cur[0] + dx, cur[1] + dy)
                edge_points.remove(cur)
                ans.append(cur)
                break
        else:
            break

    return ans


def get_edge_points(piece):
    edge_points = copy.deepcopy(piece)
    for x, y in piece:
        if (
            (x + 1, y) in piece
            and (x, y + 1) in piece
            and (x - 1, y) in piece
            and (x, y - 1) in piece
        ):
            edge_points.remove((x, y))
    return edge_points


def write_svg_path(s, piece, color, smooth_type=1):
    # not drawing small groups, will show the background color
    # if len(piece) < 10: continue
    edge_points = get_edge_points(piece)
    edge_points = get_closed_path(edge_points)
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
    s.write(f'Z" stroke="none" fill="rgb({color[0]},{color[1]},{color[2]})" />\n')


def png2svg(image, sm):
    M, N, _ = image.shape
    s = StringIO()
    s.write(svg_header(M, N))

    # collect contiguous pixel groups by traversing image
    regions = grid_func.get_same_color_regions(image, M, N)

    for piece, color in regions:
        write_svg_path(s, piece, color, smooth_type=sm)

    s.write("</svg>\n")
    return s.getvalue()


if __name__ == "__main__":
    # Warning: notice the image path (check your workspace directory)
    img = cv2.imread("png/128/emoji_u1f3c2_1f3fc.png")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    svg_image = png2svg(img)

    with open("result.svg", "w") as fh:
        fh.write(svg_image)

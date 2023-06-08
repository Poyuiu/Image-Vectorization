import cv2
import numpy as np
import matplotlib.pyplot as plt
from io import StringIO
from scipy import interpolate

# parameters
STEP = 4       # for smoothing
DIST_TH = 0    # for color grouping
PIECE_TH = 25  # for not drawing small groups
PATH = 'emoji.png'

def svg_header(width, height):
    return '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n' \
           '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"\n' \
           '"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n' \
           f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg" version="1.1">\n'

def dist(color1, color2):
    # return sum((color1 - color2) ** 2) ** 0.5  # Euclidean distance
    return sum(np.abs(color1 - color2))

def get_closed_path(edge_points):
    dir = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    start = edge_points.pop(0)
    cur = start
    ans = [cur]

    while edge_points:
        for dx, dy in dir:
            if (cur[0] + dx, cur[1] + dy) in edge_points:
                cur = (cur[0] + dx, cur[1] + dy)
                edge_points.remove(cur)
                ans.append(cur)
                break
        else: break
    ans.append(start)

    return ans

def smooth(edge_points):
    ans = []
    x = [p[0] for p in edge_points]
    y = [p[1] for p in edge_points]
    if len(edge_points) > 20:
        x = x[::STEP]
        y = y[::STEP]
    tck, u = interpolate.splprep([x, y], k=3, s=0)
    u_new = np.linspace(0, 1, num=1000)
    x_new, y_new = interpolate.splev(u_new, tck)

    for i in range(len(x_new)):
        ans.append((x_new[i], y_new[i]))

    return ans

def png2svg(image):
    M, N, _ = image.shape
    s = StringIO()
    s.write(svg_header(M, N))

    # collect contiguous pixel groups
    dir = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    visited = np.zeros((M, N))
    region = []

    for i in range(M):
        for j in range(N):
            if visited[i, j]: continue
            visited[i, j] = 1
            color = tuple(image[i, j])
            
            piece = []
            in_piece = np.zeros((M+1, N+1))
            queue = [(i, j)]
            while queue:
                cur = queue.pop()
                for dx, dy in dir:
                    neighbor = (cur[0] + dx, cur[1] + dy)
                    if neighbor[0] < 0 or neighbor[0] >= M or neighbor[1] < 0 or neighbor[1] >= N: continue
                    if visited[neighbor]: continue
                    # give a threshold
                    if dist(image[cur], image[neighbor]) > DIST_TH: continue
                    queue.append(neighbor)
                    visited[neighbor] = 1
                if not in_piece[cur]:
                    piece.append(cur)
                    in_piece[cur] = 1
                if not in_piece[cur[0], cur[1] + 1]:
                    piece.append((cur[0], cur[1] + 1))
                    in_piece[cur[0], cur[1] + 1] = 1
                if not in_piece[cur[0] + 1, cur[1] + 1]:
                    piece.append((cur[0] + 1, cur[1] + 1))
                    in_piece[cur[0] + 1, cur[1] + 1] = 1
                if not in_piece[cur[0] + 1, cur[1]]:
                    piece.append((cur[0] + 1, cur[1]))
                    in_piece[cur[0] + 1, cur[1]] = 1

            # we can determine the color later
            region.append((piece, color))

    for piece, color in region:
        # not drawing small groups, will show the background color
        if len(piece) < PIECE_TH: continue
        edge_points = piece[:]
        for x, y in piece:
            if (x+1, y) in piece and (x, y+1) in piece and (x-1, y) in piece and (x, y-1) in piece and \
               (x+1, y+1) in piece and (x+1, y-1) in piece and (x-1, y-1) in piece and (x-1, y+1) in piece:
                edge_points.remove((x, y))

        edge_points = get_closed_path(edge_points)

        edge_points = smooth(edge_points)

        s.write('<path d="')
        start = edge_points.pop(0)
        s.write(f'M {start[1]} {start[0]} ')
        for p in edge_points:
            s.write(f'L {p[1]} {p[0]} ')
        s.write('Z" stroke="none" fill="rgb(%d,%d,%d)" />\n' % color)
        
    s.write('</svg>\n')
    return s.getvalue()

def main():
    img = cv2.imread(PATH)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    svg_image = png2svg(img)
    with open("result.svg", "w") as fh:
        fh.write(svg_image)

if __name__ == '__main__':
    main()

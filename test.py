import cv2
import numpy as np
import matplotlib.pyplot as plt
from io import StringIO

def svg_header(width, height):
    return '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n' \
           '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"\n' \
           '"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n' \
           f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg" version="1.1">\n'

def dist(color1, color2):
    # return sum((color1 - color2) ** 2) ** 0.5  # Euclidean distance
    return sum(np.abs(color1 - color2))

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
        else: break

    return ans

def smooth(edge_points):
    return edge_points

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
                    # give a threshold: change '!= 0' to '> 40'
                    if dist(image[cur], image[neighbor]) != 0: continue
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
        # if len(piece) < 10: continue
        edge_points = piece.copy()
        for x, y in piece:
            if (x+1, y) in piece and (x, y+1) in piece and (x-1, y) in piece and (x, y-1) in piece:# and \
               #(x+1, y+1) in piece and (x+1, y-1) in piece and (x-1, y-1) in piece and (x-1, y+1) in piece:
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

img = cv2.imread('emoji_1.png')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
svg_image = png2svg(img)

with open("result.svg", "w") as fh:
    fh.write(svg_image)
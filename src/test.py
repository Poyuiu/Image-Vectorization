import os
import cv2
import numpy as np

import k_means
import png2svg_func
import svg2png_func
import mse_func

# cd src
directory = 'C:/Users/user/Documents/GitHub/Image-Vectorization/png/128'
store_dir = 'C:/Users/user/Documents/GitHub/Image-Vectorization/out_svg'

# file_num = len(os.listdir(directory))  # 3458
total = 0
cnt = 0

for filename in os.listdir(directory):
    original = cv2.imread(directory + '/' + filename, cv2.IMREAD_UNCHANGED)

    M, N, C = original.shape
    transparent = np.zeros((M, N))
    if C == 4:
        for i in range(M):
            for j in range(N):
                if original[i, j, 3] == 0:
                    transparent[i, j] = 1

    img = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
    img = k_means.coverting_img(img, 32)
    img = png2svg_func.smooth_detail(img)

    if C == 4:
        for i in range(M):
            for j in range(N):
                if transparent[i, j]:
                    img[i, j] = np.array([255, 255, 255])

    img = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_RGB2BGR)
    svg_image = png2svg_func.png2svg(img, 1)

    new_filename = filename[:-4]
    with open(f'{store_dir}/{new_filename}.svg', 'w') as fh:
        fh.write(svg_image)

    svg2png_func.svg2png(f'{store_dir}/{new_filename}.svg')
    result = cv2.imread("result.png")
    MSE = mse_func.calculate_mse(original, result)  # BGR
    total += MSE
    cnt += 1
    print(f"{filename}: MSE = {MSE}, cnt = {cnt}, temp average: {total / cnt}")


print(f"Average MSE of all the png files: {total / cnt}")

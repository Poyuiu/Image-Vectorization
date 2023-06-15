import os
import cv2
import numpy as np

import k_means
import png2svg_func
import svg2png_func
import mse_func

# cd src
directory = '../png/128'

total = 0
# file_num = len(os.listdir(directory))  # 3458
cnt = 0

for filename in os.listdir(directory):
    original = cv2.imread(directory + '/' + filename)
    img = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
    img = k_means.coverting_img(img, 32)
    img = png2svg_func.smooth_detail(img)

    img = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_RGB2BGR)
    svg_image = png2svg_func.png2svg(img, 1)
    with open('result.svg', 'w') as fh:
        fh.write(svg_image)

    svg2png_func.svg2png('result.svg')
    result = cv2.imread('result.png')
    MSE = mse_func.calculate_mse(original, result)  # BGR
    total += MSE
    print(f'{filename}: MSE = {MSE}')

    cnt += 1
    if cnt == 5: break
    
# print(f'Average MSE of all the png files: {total / file_num}')

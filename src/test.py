import os
import cv2
import numpy as np

import k_means
import png2svg_func
import svg2png_func
import mse_func

# cd src
directory = r"C:\Users\ryanp\D_\multimedia\Image-Vectorization\Image-Vectorization\png\128"
store_dir = r"C:\Users\ryanp\D_\multimedia\Image-Vectorization\Image-Vectorization\out_svg"

total = 0
# file_num = len(os.listdir(directory))  # 3458
cnt = 0

for filename in os.listdir(directory):
    original = cv2.imread(directory + '\\' + filename)
    img = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
    img = k_means.coverting_img(img, 32)
    img = png2svg_func.smooth_detail(img)

    img = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_RGB2BGR)
    svg_image = png2svg_func.png2svg(img, 1)
    
    new_filename = filename[:-3]
    with open(store_dir + '\\' + new_filename + "svg", 'w') as fh:
        fh.write(svg_image)

    
    svg2png_func.svg2png(store_dir + '\\' + new_filename + "svg")
    result = cv2.imread('result.png')
    MSE = mse_func.calculate_mse(original, result)  # BGR
    total += MSE
    cnt += 1
    print(f'{filename}: MSE = {MSE}, cnt = {cnt}')

    
    
print(f'Average MSE of all the png files: {total / cnt}')

import os
import cv2
import numpy as np

import k_means
import png2svg_func

# cd src
directory = 'C:/Users/user/Documents/GitHub/Image-Vectorization/png/wild'
store_dir = 'C:/Users/user/Documents/GitHub/Image-Vectorization/out_wild_svg'
# file_num = len(os.listdir(directory))  # 10

for filename in os.listdir(directory):
    original = cv2.imread(directory + '/' + filename)
    img = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
    img = k_means.coverting_img(img, 32)
    img = png2svg_func.smooth_detail(img)

    img = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_RGB2BGR)
    svg_image = png2svg_func.png2svg(img, 1)

    new_filename = filename[:-4]
    with open(f'{store_dir}/{new_filename}.svg', 'w') as fh:
        fh.write(svg_image)
        
    print(f'{filename} finished')


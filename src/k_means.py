import numpy as np
import matplotlib.pyplot as plt
import cv2
from sklearn.cluster import KMeans

def coverting_img(img, k_color):
    width,height,channel = img.shape
    pixels = img.reshape(-1, img.shape[2])
    kmeans_model = KMeans(n_clusters=k_color) # we shall retain only 7 colors
    cluster_labels = kmeans_model.fit_predict(pixels)
    rgb_cols = kmeans_model.cluster_centers_.round(0).astype(int)
    img_quant = np.reshape(rgb_cols[cluster_labels],(width,height,channel))
    return img_quant
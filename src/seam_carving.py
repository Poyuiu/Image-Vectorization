import numpy as np
from PIL import Image


def resize_image(image, new_height, new_width):
    # Convert the image to a NumPy array
    image_array = np.array(image)

    # Get the current dimensions of the image
    height, width, _ = image_array.shape

    # Calculate the number of seams to remove
    seam_height = height - new_height
    seam_width = width - new_width

    # Perform seam carving
    if seam_height > 0:
        image_array = remove_vertical_seams(image_array, seam_height)
    elif seam_height < 0:
        image_array = add_vertical_seams(image_array, abs(seam_height))

    if seam_width > 0:
        image_array = remove_horizontal_seams(image_array, seam_width)
    elif seam_width < 0:
        image_array = add_horizontal_seams(image_array, abs(seam_width))

    # Convert the resulting array back to an image
    resized_image = Image.fromarray(image_array)

    return resized_image


def remove_vertical_seams(image, num_seams):
    for _ in range(num_seams):
        energy_map = calculate_energy_map(image)
        seam_mask = find_vertical_seam(energy_map)
        image = remove_seam(image, seam_mask)

    return image


def add_vertical_seams(image, num_seams):
    for _ in range(num_seams):
        energy_map = calculate_energy_map(image)
        seam_mask = find_vertical_seam(energy_map)
        image = add_seam(image, seam_mask)

    return image


def remove_horizontal_seams(image, num_seams):
    # Transpose the image array to process horizontal seams as vertical seams
    image = np.transpose(image, (1, 0, 2))

    image = remove_vertical_seams(image, num_seams)

    # Transpose the image array back to its original orientation
    image = np.transpose(image, (1, 0, 2))

    return image


def add_horizontal_seams(image, num_seams):
    # Transpose the image array to process horizontal seams as vertical seams
    image = np.transpose(image, (1, 0, 2))

    image = add_vertical_seams(image, num_seams)

    # Transpose the image array back to its original orientation
    image = np.transpose(image, (1, 0, 2))

    return image


def calculate_energy_map(image):
    # Implement your energy map calculation logic here
    # This can be done using various techniques such as gradient magnitude calculation

    # Example code for energy map calculation using the Sobel operator
    gray_image = Image.fromarray(image).convert("L")  # Convert the image to grayscale
    gradient_x = np.abs(np.asarray(gray_image.filter(ImageFilter.FIND_EDGES))).astype(np.float32)
    gradient_y = np.abs(np.asarray(gray_image.transpose(Image.TRANSPOSE))).astype(np.float32)
    energy_map = gradient_x + gradient_y

    return energy_map


def find_vertical_seam(energy_map):
    # Implement your vertical seam finding logic here
    # This can be done using dynamic programming (e.g., dynamic programming or backward energy)

    # Example code for finding the vertical seam using dynamic programming (backward energy)
    height, width = energy_map.shape
    dp = np.zeros((height, width))
    for i in range(1, height):
        for j in range(width):
            if j == 0:
                dp[i, j] = energy_map[i, j] + min(dp[i-1, j], dp[i-1, j+1])
            elif j == width - 1:
                dp[i, j] = energy_map[i, j] + min(dp[i-1, j-1], dp[i-1, j])
            else:
                dp[i, j] = energy_map[i, j] + min(dp[i-1, j-1], dp[i-1, j], dp[i-1, j+1])

    # Find the optimal vertical seam by backtracking
    seam_mask = np.zeros((height,), dtype=np.int32)
    seam_mask[-1] = np.argmin(dp[-1])
    for i in range(height - 2, -1, -1):
        j = seam_mask[i + 1]
        if j == 0:
            seam_mask[i] = j + np.argmin(dp[i, j:j + 2])
        elif j == width - 1:
            seam_mask[i] = j - 1 + np.argmin(dp[i, j - 1:j + 1])
        else:
            seam_mask[i] = j - 1 + np.argmin(dp[i, j - 1:j + 2])

    return seam_mask


def remove_seam(image, seam_mask):
    height, width, _ = image.shape
    mask = np.ones((height, width - 1), dtype=np.bool)
    for row in range(height):
        col = np.where(seam_mask[row] == True)[0][0]
        mask[row, :col] = False
        mask[row, col:] = True
        image[row] = image[row][mask[row]].reshape((width - 1, -1))

    return image


def add_seam(image, seam_mask):
    height, width, _ = image.shape
    mask = np.ones((height, width + 1), dtype=np.bool)
    for row in range(height):
        col = np.where(seam_mask[row] == True)[0][0]
        mask[row, :col + 1] = False
        mask[row, col + 1:] = True
        image[row] = np.insert(image[row], col + 1, image[row, col], axis=0)
        image[row] = image[row][mask[row]].reshape((width + 1, -1))

    return image

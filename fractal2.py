import concurrent.futures
import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
from scipy import ndimage

candidates = [
    (0, 0),    # No transformation (direction: 0, angle: 0 degrees)
    (1, 0),   # Flip horizontally (direction: 1, angle: 0 degrees)
    (0, 180),  # Flip vertically (direction: 0, angle: 180 degrees)
    # Add more transformations as needed
]


def reduce(img, factor):
    return ndimage.zoom(img, 1/factor, order=1)

def rotate(img, angle):
    return ndimage.rotate(img, angle, reshape=False)

def flip(img, direction):
    return np.flip(img, axis=direction)

def apply_transformation(img, direction, angle, contrast=1.0, brightness=0.0):
    transformed_img = rotate(flip(img, direction), angle)
    return contrast * transformed_img + brightness

def generate_all_transformed_blocks(img, source_size, destination_size, step):
    factor = source_size // destination_size
    transformed_blocks = []
    for k in range(0, img.shape[0] - source_size + 1, step):
        for l in range(0, img.shape[1] - source_size + 1, step):
            S = reduce(img[k:k + source_size, l:l + source_size], factor)
            for direction, angle in candidates:
                transformed_blocks.append((k, l, direction, angle, S))
    return transformed_blocks

def compress_block(img, destination_size, i, j, transformed_blocks):
    min_d = float('inf')
    D = img[i * destination_size:(i + 1) * destination_size, j * destination_size:(j + 1) * destination_size]
    best_transformation = None
    
    for k, l, direction, angle, S in transformed_blocks:
        contrast, brightness = find_contrast_and_brightness2(D, S)
        S = contrast * S + brightness
        d = np.sum(np.square(D - S))
        if d < min_d:
            min_d = d
            best_transformation = (k, l, direction, angle, contrast, brightness)
    print(f"Block ({i}, {j}) processed.")
    return best_transformation

def compress(img, source_size, destination_size, step):
    transformations = []
    transformed_blocks = generate_all_transformed_blocks(img, source_size, destination_size, step)
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_position = {
            executor.submit(compress_block, img, destination_size, i, j, transformed_blocks): (i, j)
            for i in range(img.shape[0] // destination_size)
            for j in range(img.shape[1] // destination_size)
        }
        
        for future in concurrent.futures.as_completed(future_to_position):
            i, j = future_to_position[future]
            try:
                transformation = future.result()
                transformations.append(transformation)
            except Exception as e:
                print(f"Error in block ({i}, {j}): {e}")
                
    return transformations


def decompress(transformations, source_size, destination_size, step, nb_iter=8):
    factor = source_size // destination_size
    height = len(transformations) * destination_size
    width = len(transformations[0]) * destination_size
    iterations = [np.random.randint(0, 256, (height, width))]

    for i_iter in range(nb_iter):
        print(i_iter)
        cur_img = np.zeros((height, width))
        for i in range(len(transformations)):
            for j in range(len(transformations[i])):
                k, l, flip, angle, contrast, brightness = transformations[i][j]
                S = reduce(iterations[-1][k * step:k * step + source_size, l * step:l * step + source_size], factor)
                D = apply_transformation(S, flip, angle, contrast, brightness)
                cur_img[i * destination_size:(i + 1) * destination_size, j * destination_size:(j + 1) * destination_size] = D
        iterations.append(cur_img)

    return iterations

def find_contrast_and_brightness2(D, S):
    A = np.concatenate((np.ones((S.size, 1)), np.reshape(S, (S.size, 1))), axis=1)
    b = np.reshape(D, (D.size,))
    x, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
    return x[1], x[0]

def open_file():
    file_path = filedialog.askopenfilename()
    img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    return img

def main():
    root = tk.Tk()
    root.withdraw()

    img = open_file()

    source_size = 8
    destination_size = 2
    step = 2

    transformations = compress(img, source_size, destination_size, step)
    decompressed_images = decompress(transformations, source_size, destination_size, step)

    for i, image in enumerate(decompressed_images):
        cv2.imshow(f"Iteration {i}", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    root.mainloop()

def main():
    root = tk.Tk()
    root.withdraw()

    img = open_file()

    source_size = 8
    destination_size = 2
    step = 2

    transformations = compress(img, source_size, destination_size, step)
    decompressed_images = decompress(transformations, source_size, destination_size, step)

    for i, image in enumerate(decompressed_images):
        cv2.imshow(f"Iteration {i}", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    root.mainloop()

if __name__ == "__main__":
    main()

import numpy as np
from PIL import Image
from skimage import color
from pathlib import Path

def count_files_in_directory(directory):
    # Create a Path object for the specified directory
    path = Path(directory)

    # Use the glob method to list all files in the directory
    files = [f for f in path.iterdir() if f.is_file()]

    return len(files)

width = 600
height = 400

directory = './source_images/'
#num_files = count_files_in_directory(directory)

image_stack = np.array(np.zeros(width * height))
try:
    for i in range(1, 10000):
        image = Image.open(F'./source_images/{i}.jpg')
        print(i)
        image_array = np.array(image)
        imagegrey = color.rgb2gray(image_array)
        reshaped_array = imagegrey.reshape(-1, 1)
        image_stack = np.append(image_stack, reshaped_array, axis=1)
except:
    print("End of files reached.")

print(image_stack.shape)


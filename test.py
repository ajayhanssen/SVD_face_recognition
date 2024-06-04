import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

# Path for training images
Path2 = './source_images/'
files2 = os.listdir(Path2)
images = []

# Read all images, convert to grayscale, and flatten
for name in files2:
    temp = cv2.imread(Path2 + name)
    temp = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
    images.append(temp.flatten())

# Normalize by subtracting the mean
images = np.array(images)
mu = np.mean(images)
images = images - mu
images = images.T
print("Images shape:", images.shape)

# Perform SVD
u, s, v = np.linalg.svd(images, full_matrices=False)
print("Shapes - U:", u.shape, "S:", s.shape, "V:", v.shape)

# Read and preprocess the test image
test = cv2.imread('./test_images/')
test = cv2.cvtColor(test, cv2.COLOR_BGR2GRAY)

# Flatten and normalize the test image
img = test.reshape(1, -1)
img = img - mu
img = img.T

# Project the test image into PCA space
dot_test = np.dot(u.T, img).flatten()

# Project training images into PCA space
dot_train = np.dot(u.T, images)

# Calculate the norm (distance) between the test image and all training images
dists = np.linalg.norm(dot_train - dot_test[:, np.newaxis], axis=0)

# Find the index of the minimum distance
min_index = np.argmin(dists)
print("Minimum distance:", dists[min_index])

# Retrieve the filename of the best-matching training image
predicted_image = files2[min_index]
print("The predicted face is:", predicted_image)
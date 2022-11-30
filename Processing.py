import math
import numpy as np
from scipy.stats import beta
import cv2
from matplotlib import pyplot as plt
from gridding import draw_grid


import matplotlib.animation as animation

import math

RED_SENSITIVITY = 0.299
GREEN_SENSITIVITY = 0.587
BLUE_SENSITIVITY = 0.114

def pixel_brightness(pixel):
    assert 3 == len(pixel)
    r, g, b = pixel
    return math.sqrt(RED_SENSITIVITY * r ** 2 + GREEN_SENSITIVITY * g ** 2 + BLUE_SENSITIVITY * b ** 2) #Darel Rex Finley Factor

def rgb_matrix(img,r,c):


    grid = [[[] for cnt in range(c)] for counter in range(r)]
    # print(grid)
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            grid[x][y].append([])
            for z in range(3):
                grid[x][y][0].append(0)
            grid[x][y].append([0])
    # print(grid)
    # print(len(img),len(img[0]))
    d = len(img) * len(img[0]) / (r * c)
    rd = len(img) / r
    cd = len(img[0]) / c
    # print(grid)
    for row in range(len(img)):
        for col in range(len(img[0])):
            # print(row // rd)
            # print(col // cd)

            pixel = img[row][col]
            # print(pixel)
            grid[int(row // rd)][int(col // cd)][0][0] += pixel[0]
            grid[int(row // rd)][int(col // cd)][0][1] += pixel[1]
            grid[int(row // rd)][int(col // cd)][0][2] += pixel[2]
            grid[int(row // rd)][int(col // cd)][1][0] += 1
            # print(grid)
    # print(grid)
    # print(grid[0][0][0][0],grid[0][0][1],grid[0][0][0][0]/grid[0][0][1])

    for x in range(r):
        for y in range(c):
            grid[x][y][0][0] = grid[x][y][0][0] / grid[x][y][1][0]
            grid[x][y][0][1] = grid[x][y][0][1] / grid[x][y][1][0]
            grid[x][y][0][2] = grid[x][y][0][2] / grid[x][y][1][0]

    print('\n\n\n\n\n\n')
    # print(grid)
    return grid


def image_brightness(img,r,c):

    grid = [[[0 for x in range(2)] for y in range(c)] for counter in range(r)]
    # print(grid)
    # print(len(img),len(img[0]))
    d = len(img)*len(img[0])/(r*c)
    rd = len(img)/r
    cd = len(img[0])/c
    for row in range(len(img)):
        for col in range(len(img[0])):
            # print(row // rd)
            # print(col // cd)
            pixel = img[row][col]
            grid[int(row//rd)][int(col//cd)][0]+=pixel_brightness(pixel)
            grid[int(row//rd)][int(col//cd)][1]+=1
    print('\n\n\nImage Energy Intensity\n\n')
    print(grid)
    for x in range(r):
        for y in range(c):
            grid[x][y] = grid[x][y][0]/grid[x][y][1]


    # print(grid)
    return grid



def convert_to_brightness_image(image: np.ndarray) -> np.ndarray:
    if image.dtype == np.uint8:
        raise ValueError("uint8 is not a good dtype for the image")

    return np.sqrt(
        image[..., 0] ** 2 * RED_SENSITIVITY
        + image[..., 1] ** 2 * GREEN_SENSITIVITY
        + image[..., 2] ** 2 * BLUE_SENSITIVITY
    )
def get_resolution(image: np.ndarray):
    height, width = image.shape[:2]
    return height * width

def brightness_histogram(image: np.ndarray) -> np.ndarray:
    nr_of_pixels = get_resolution(image)
    brightness_image = convert_to_brightness_image(image)
    hist, _ = np.histogram(brightness_image, bins=256, range=(0, 255))
    plt.hist(hist,density=True, facecolor='g', alpha=0.75)
    plt.xlabel('Brightness')
    plt.ylabel('Image Paramx')

    plt.title("Birghtness Histogram")

    plt.show()

    return hist / nr_of_pixels
def distribution_pmf(dist: any, start: float, stop: float, nr_of_steps: int):
    xs = np.linspace(start, stop, nr_of_steps)
    ys = dist.pdf(xs)
    # divide by the sum to make a probability mass function
    return ys / np.sum(ys)
def correlation_distance(
    distribution_a: np.ndarray, distribution_b: np.ndarray
) -> float:
    dot_product = np.dot(distribution_a, distribution_b)
    squared_dist_a = np.sum(distribution_a ** 2)
    squared_dist_b = np.sum(distribution_b ** 2)
    return dot_product / math.sqrt(squared_dist_a * squared_dist_b)
def compute_hdr(cv_image: np.ndarray):
    img_brightness_pmf = brightness_histogram(np.float32(cv_image))
    ref_pmf = distribution_pmf(beta(2, 2), 0, 1, 256)
    return correlation_distance(ref_pmf, img_brightness_pmf)

# image_brightness(img)



def energyConsumption(image):
    energyCount = image_brightness(image,10,10)
    toneMappingScore = compute_hdr(image)
    if toneMappingScore <=0.02:
        print('Cannot be analysed')
        return
    print('Average Energy Count: ')
    print(energyCount)
    print('Confidence Level: ' + str((toneMappingScore*100)+80))
    return energyCount


Delhi = 'Satellite Images/Delhi/Delhi_SAT1.jpg'
Berlin = 'Satellite Images/Berlin_SAT1.jpg'
test = 'Satellite Images/testimg2.jpg'
SanFrancisco = 'Satellite Images/SanFrancisco_SAT1.jpg'

# img = cv2.imread(Delhi)
# energyConsumption(img)
# img = cv2.imread(Berlin)
# energyConsumption(img)
img = cv2.imread(Delhi)
# image_brightness(img,10,10)
rgb_matrix(img,10,10)
# draw_grid(img,[10,10], color=(255, 0, 0), thickness=2)
# testimg = cv2.imread(test)
# energyConsumption(testimg)

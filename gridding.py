import cv2 as cv2
import numpy as np


def draw_grid(img, grid_shape, color=(0, 255, 0), thickness=1):
    h, w, _ = img.shape
    rows, cols = grid_shape
    dy, dx = h / rows, w / cols

    # draw vertical lines
    for x in np.linspace(start=dx, stop=w-dx, num=cols-1):
        x = int(round(x))
        cv2.line(img, (x, 0), (x, h), color=color, thickness=thickness)

    # draw horizontal lines
    for y in np.linspace(start=dy, stop=h-dy, num=rows-1):
        y = int(round(y))
        cv2.line(img, (0, y), (w, y), color=color, thickness=thickness)
    img = cv2.resize(img, (960, 540))
    cv2.imshow('image', img)

    # waits for user to press any key
    # (this is necessary to avoid Python kernel form crashing)
    cv2.waitKey(5000)

    # closing all open windows
    cv2.destroyAllWindows()
    return img


    # SanFrancisco = 'Satellite Images/SanFrancisco_SAT1.jpg'
    # img = cv2.imread(SanFrancisco)
    # processed_img = draw_grid(img,[10,10])
    # cv2.imshow('image', processed_img)
    #
    # # waits for user to press any key
    # # (this is necessary to avoid Python kernel form crashing)
    # cv2.waitKey(0)
    #
    # # closing all open windows
    # cv2.destroyAllWindows()

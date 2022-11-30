import math
import numpy as np
from scipy.stats import beta
import cv2
from matplotlib import pyplot as plt
from gridding import draw_grid

im = cv2.imread('Satellite Images/London/overlayedimg.jpg')
font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(im, 'Superimposed Analysis', (0,0), font, 3, (0, 0, 255), 2, cv2.LINE_AA)
cv2.imwrite('anotated.jpg',im)
cv2.imshow('image', im)
cv2.waitKey(0)
cv2.destroyAllWindows()
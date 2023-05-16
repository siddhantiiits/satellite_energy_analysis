import pytesseract
from PIL import Image
import cv2
import urllib
import urllib.request
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/5.3.0/bin/tesseract'
img = Image.open('test.jpeg')
image = np.asarray(img, dtype="uint8")
image = cv2.imdecode(image, cv2.IMREAD_COLOR)
retval, img = cv2.threshold(img,200,255, cv2.THRESH_BINARY)
img = cv2.resize(img,(0,0),fx=3,fy=3)
img = cv2.GaussianBlur(img,(11,11),0)
img = cv2.medianBlur(img,9)
cv2.imshow('asd',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
txt = pytesseract.image_to_string(img)
print('recognition:', txt)

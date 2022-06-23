import numpy as np
import cv2



image = cv2.imread("module/folder/frame37.jpg")

lower_white = np.array([200, 200, 200], dtype=np.uint8)
upper_white = np.array([255, 255, 255], dtype=np.uint8)
mask = cv2.inRange(image, lower_white, upper_white) # could also use threshold
res = cv2.bitwise_not(image, image, mask)
cv2.imshow('res', res)
lower_white = np.array([190, 190, 190], dtype=np.uint8)
upper_white = np.array([255, 255, 255], dtype=np.uint8)
mask = cv2.inRange(image, lower_white, upper_white) # could also use threshold
res = cv2.bitwise_not(image, image, mask)
cv2.imshow('res2', res)
lower_white = np.array([180, 180, 180], dtype=np.uint8)
mask = cv2.inRange(image, lower_white, upper_white) # could also use threshold
res = cv2.bitwise_not(image, image, mask)
cv2.imshow('res2', res)

cv2.waitKey(0)
cv2.destroyAllWindows()
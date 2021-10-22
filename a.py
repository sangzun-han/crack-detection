import numpy as np
import cv2
from matplotlib import pyplot as plt


img = cv2.imread('Input-Set/Cracked_06.jpg')



rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 30))
threshed = cv2.morphologyEx(img, cv2.MORPH_CLOSE, rect_kernel)


imgContours, Contours, Hierarchy = cv2.findContours(threshed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
for cnt in Contours:
    hull = cv2.convexHull(cnt)
    cv2.drawContours(threshed, [hull], -1, (0, 0, 255), 1) 


cv2.imwrite('a/Cracked_07.jpg', threshed)


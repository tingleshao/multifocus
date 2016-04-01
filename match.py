import numpy as np
import cv2
from matplotlib import pyplot as plt

img1 = cv2.imread('box.png', 0)
img2 = cv2.imread('box_in_scene.png', 0)

sift = cv2.ORB()

kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)

bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
matches = bf.Match(des1, des2)

matches = sorted(matches)
good = []
for m,n in matches:
    if m.distance < 0.75*n.distance:
        good.append([m])
		
		
img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good, flags=2)

plt.imshow(img3), plt.show()
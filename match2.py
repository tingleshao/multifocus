import cv2
import numpy as np

im1 = cv2.imread("img1.jpg")
im2 = cv2.imread("img2.jpg")

im1_gray = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
im2_gray = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)

sz = im1.shape

warp_mode = cv2.MOTION_TRANSLATION

if warp_mode == cv2.MOTION_HOMOGRAPHY:
    warp_matrix = np.eye(3,3,dtype=np.float32)
else:
    warp_matrix = np.eye(2,3, dtype=np.float32)
	
number_of_iteration = 5000

termination_eps = 1e-10

criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, number_of_iteration, termination_eps)

(cc,warp_matrix) = cv2.findTransformECC(im1_gray, im2_gray, warp_matrix, warp_mode, criteria)

if warp_mode == cv2.MOTION_HOMOGRAPHY:
    im2_aligned = cv2.warpPerspective(im2, warp_matrix, (sz[1], sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
else:
    im2_aligned = cv2.warpAffine(im2, warp_matrix, (sz[1], sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP);

cv2.imshow("image 1", im1)
cv2.imshow("image 2", im2)
cv2.imshow("aligned image 2", im2_aligned)
cv2.waitKey(0)
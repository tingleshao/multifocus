# this script captures one frame and save it as ppm

import sys
import numpy as np
import cv2

print sys.argv 
if len(sys.argv) == 1:
    print "no image name is specified!"
    sys.exit(0)


def rotateImage(image, angle):
    image_center = tuple(np.array(image.shape)/2)
    rot_mat = cv2.getRotationMatrix2D(center=(image_center[1],image_center[0]),angle=angle,scale=1.0)
    result = cv2.warpAffine(src=image, M=rot_mat, dsize=(image.shape[1], image.shape[0]), flags=cv2.INTER_LINEAR)
    return result

	
img_name = sys.argv[1]
cap = cv2.VideoCapture(1)

cap.set(3, 2048)
cap.set(4, 1536)

ret, frame = cap.read()
frame = rotateImage(frame, 180)

cv2.imwrite(img_name, frame)
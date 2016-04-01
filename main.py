import cv2
import numpy as np

import os


def rotateImage(image, angle):
    image_center = tuple(np.array(image.shape)/2)
    rot_mat = cv2.getRotationMatrix2D(center=(image_center[1],image_center[0]),angle=angle,scale=1.0)
    result = cv2.warpAffine(src=image, M=rot_mat, dsize=(image.shape[1], image.shape[0]), flags=cv2.INTER_LINEAR)
    return result

	
def makingDir(index):
    directory = 'image_saved/pair' + str(index)
    if not os.path.exists(directory):
	    os.makedirs(directory)    
	
refPt = []

def mouseZoom(event, x, y, flags, param):
    global refPt
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x,y)]
        print refPt
	
cv2.namedWindow("preview")
cv2.setMouseCallback("preview", mouseZoom)
vc = cv2.VideoCapture(1)
vc.set(3,1024)
vc.set(4, 768)
vc2 = cv2.VideoCapture(2)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False
	
in_focus_saved = False

while rval:
    #print frame.shape
    frame = rotateImage(frame, 180)
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    rval2, frame2 = vc2.read()
    print frame2
    key = cv2.waitKey(20)
    if key != -1:
        print key
	if key == 97:
	    if not in_focus_saved: # take pics 
	        # make dir
		    index = 2
		    makingDir(index)
		    cv2.imwrite('image_saved/pair' + str(index) + '/infocus.jpg', frame)
		    in_focus_saved = True
	    else:
		    # save the out of focus one 
			cv2.imwrite('image_saved/pair' + str(index) + '/outfocus.jpg', frame) 
	if key == 115: # goes into interactive view mode
	    # TODO: firstly load the out of focus one 
		#       when clicked on a region, zoom in to that region, and replace the content with the focused one
		#       may display another "something" showing the result of blending the out of focus one with the in focus one 
	    print "s pressed"
    if key == 27: # exit on ESC
        break
cv2.destroyWindow("preview")


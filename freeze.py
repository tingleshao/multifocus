import cv2
import numpy as np


import os

index = 1 

image_dir = 'image_saved/pair' + str(index) + '/'
out_focus = cv2.imread(image_dir + 'outfocus.jpg')
in_focus = cv2.imread(image_dir + 'infocus.jpg')

out_focus_copy = out_focus.copy()

def blendImg():
    return False

refPt = []
focus_now = False

def blend(in_focus, out_focus, pt):
# blend the in focus image with the out foucus image, centered as the given point 
    # 200 * 100 roi 
	# upper left: (pt.x - 100 or 0, pt.y - 50 or 0)
	# upper right: (pt.x + 100 or width, pt.y - 50 or 0)
	# lower left: (pt.x - 100 or 0, pt.y + 50 or height)
	# lower right: (pt.x + 100 or width, pt.y + 50 or height)
    width = out_focus.shape[1]
    height = out_focus.shape[0]
    upper_left_x = pt[0][0] - 100 if pt[0][0] - 100 > -1 else 0 
    upper_left_y = pt[0][1] - 50 if pt[0][1] - 50 > -1 else 0	
    lower_right_x = pt[0][0] + 100 if pt[0][0] + 100 < width else width - 1
    lower_right_y = pt[0][1] + 50 if pt[0][1] + 50 < height else height - 1
    out_focus_copy[upper_left_y:lower_right_y, upper_left_x:lower_right_x] = in_focus[upper_left_y:lower_right_y, upper_left_x:lower_right_x]	
    #in_focus_roi = in_focus.copy()
    return out_focus_copy

	
def mouseZoom(event, x, y, flags, param):
    global refPt, focus_now, out_focus_copy
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x,y)]
        print refPt
	# change the in_focus image into a blending of in_focus image and out_focus image 
	out_focus_copy = blend(in_focus, out_focus_copy, refPt)
	focus_now = not focus_now

cv2.namedWindow("zoom")
cv2.setMouseCallback("zoom", mouseZoom)


while True:
    if focus_now:
		out_focus_copy = out_focus.copy()
    cv2.imshow("zoom", out_focus_copy)
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


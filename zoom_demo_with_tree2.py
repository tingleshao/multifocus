import matplotlib.pyplot as plt
import cv2
import numpy as np


image_dir = 'image_saved/exp00/'

mm_25_00 = cv2.imread(image_dir + '25mm_00.ppm')
mm_25_01 = cv2.imread(image_dir + '25mm_01.ppm')
mm_25_02 = cv2.imread(image_dir + '25mm_02.ppm')
mm_8_00 = cv2.imread(image_dir + '8mm_00.ppm') 

mm_25_w = 325 * 2 
mm_25_h = 246 * 2 

mm_8_w = 2048
mm_8_h = 1534

mm_25_00_x = 206 * 2 
mm_25_00_y = 304 * 2

mm_25_01_x = 372 * 2 
mm_25_01_y = 306 * 2 

mm_25_02_x = 555 * 2
mm_25_02_y = 330 * 2 


class JpegTree:
    def f(self): 
        return 'hello world'
        
    def __init__(self, data, children, upper_x, upper_y, w, h): 
        self.data = data 
        self.children = children 
        self.upper_x = upper_x  
        self.upper_y = upper_y 
        self.w = w 
        self.h = h   

    # TODO: discover a blending approach 
    def generateView(self, x, y, curr_xlim, curr_ylim):


curr_node = m_8_00_t

out_focus = mm_8_00.copy()
out_focus_copy = out_focus.copy()

xlim = out_focus.shape[1]
ylim = out_focus.shape[0]

mode = 0 # 0: zoom in, 1: zoom out

ratio = 2048 / (325 * 2)#
#ratio2 = 1024  / (mm_25_00_w - mm_25_00_x)

#fig = plt.figure()
#ax = fig.add_subplot(211)
#ax.plot(range(10))
scale = 1.5 

# TODO: based on the point and curr x / y lim, we should able to determine where we are in the tree (efficiently)
def find_tree_zoom_in_img(xlim, ylim, x, y): 
    img = None
    ratio2 = 1024  / (xlim[1] - xlim[0])

    x = x
    y = y
    if mm_25_00_x / 2 <= x <= mm_25_w / 2 + mm_25_00_x / 2 and mm_25_00_y / 2  <= y <= mm_25_h / 2+ mm_25_00_y / 2: 
        print "in zoom in mode 0!!!!!!!"
        # blend with the 25mm image 
        img = out_focus[ylim[0]:ylim[1], xlim[0]:xlim[1]]
        in_focus_x0 = xlim[0] if xlim[0] > mm_25_00_x else mm_25_00_x
        in_focus_x1 = xlim[1] if xlim[1] < mm_25_w + mm_25_00_x else mm_25_w + mm_25_00_x 
        in_focus_y0 = ylim[0] if ylim[0] > mm_25_00_y else mm_25_00_y
        in_focus_y1 = ylim[1] if ylim[1] < mm_25_h + mm_25_00_y else mm_25_h + mm_25_00_y
        real_x0 = ( in_focus_x0 - xlim[0] ) * ratio2 
        real_x1 = ( in_focus_x1 - xlim[0] ) * ratio2 
        real_y0 = ( in_focus_y0 - ylim[0] ) * ratio2 
        real_y1 = ( in_focus_y1 - ylim[0] ) * ratio2 
        in_focus_x0 = (in_focus_x0 - mm_25_00_x) * ratio 
        in_focus_x1 = (in_focus_x1 - mm_25_00_x) * ratio 
        in_focus_y0 = (in_focus_y0 - mm_25_00_y) * ratio 
        in_focus_y1 = (in_focus_y1 - mm_25_00_y) * ratio
        img = cv2.resize(img, (1024, 768)) 
        sub_img = mm_25_00[in_focus_y0:in_focus_y1, in_focus_x0:in_focus_x1]
        sub_img = cv2.resize(sub_img, (int(real_x1 - real_x0), int(real_y1 - real_y0)))
        img[real_y0:real_y1, real_x0:real_x1] = sub_img 
   #     img = cv2.resize(img, (1024, 768)) 
    elif mm_25_01_x / 2 <= x <= mm_25_w / 2 + mm_25_01_x / 2 and mm_25_01_y /2  <= y <= mm_25_h / 2+ mm_25_01_y / 2:
        print "in zoom in mode 1!!!!!!!"
        # blend with the 25mm image 
        img = out_focus[ylim[0]:ylim[1], xlim[0]:xlim[1]]
        in_focus_x0 = xlim[0] if xlim[0] > mm_25_01_x else mm_25_01_x
        in_focus_x1 = xlim[1] if xlim[1] < mm_25_w + mm_25_01_x else mm_25_w + mm_25_01_x 
        in_focus_y0 = ylim[0] if ylim[0] > mm_25_01_y else mm_25_01_y
        in_focus_y1 = ylim[1] if ylim[1] < mm_25_h + mm_25_01_y else mm_25_h + mm_25_01_y
        real_x0 = ( in_focus_x0 - xlim[0] ) * ratio2 
        real_x1 = ( in_focus_x1 - xlim[0] ) * ratio2 
        real_y0 = ( in_focus_y0 - ylim[0] ) * ratio2 
        real_y1 = ( in_focus_y1 - ylim[0] ) * ratio2 
        in_focus_x0 = (in_focus_x0 - mm_25_01_x) * ratio 
        in_focus_x1 = (in_focus_x1 - mm_25_01_x) * ratio 
        in_focus_y0 = (in_focus_y0 - mm_25_01_y) * ratio 
        in_focus_y1 = (in_focus_y1 - mm_25_01_y) * ratio
        img = cv2.resize(img, (1024, 768)) 
        sub_img = mm_25_01[in_focus_y0:in_focus_y1, in_focus_x0:in_focus_x1]
        sub_img = cv2.resize(sub_img, (int(real_x1 - real_x0), int(real_y1 - real_y0)))
        img[real_y0:real_y1, real_x0:real_x1] = sub_img 
    elif mm_25_02_x / 2 <= x <= mm_25_w / 2 + mm_25_02_x / 2 and mm_25_02_y / 2  <= y <= mm_25_h / 2+ mm_25_02_y / 2:
        print "in zoom in mode 2!!!!!!!"
        # blend with the 25mm image 
        img = out_focus[ylim[0]:ylim[1], xlim[0]:xlim[1]]
        in_focus_x0 = xlim[0] if xlim[0] > mm_25_02_x else mm_25_02_x
        in_focus_x1 = xlim[1] if xlim[1] < mm_25_w + mm_25_02_x else mm_25_w + mm_25_02_x 
        in_focus_y0 = ylim[0] if ylim[0] > mm_25_00_y else mm_25_02_y
        in_focus_y1 = ylim[1] if ylim[1] < mm_25_h + mm_25_02_y else mm_25_h + mm_25_02_y
        real_x0 = ( in_focus_x0 - xlim[0] ) * ratio2 
        real_x1 = ( in_focus_x1 - xlim[0] ) * ratio2 
        real_y0 = ( in_focus_y0 - ylim[0] ) * ratio2 
        real_y1 = ( in_focus_y1 - ylim[0] ) * ratio2 
        in_focus_x0 = (in_focus_x0 - mm_25_02_x) * ratio 
        in_focus_x1 = (in_focus_x1 - mm_25_02_x) * ratio 
        in_focus_y0 = (in_focus_y0 - mm_25_02_y) * ratio 
        in_focus_y1 = (in_focus_y1 - mm_25_02_y) * ratio
        img = cv2.resize(img, (1024, 768)) 
        sub_img = mm_25_02[in_focus_y0:in_focus_y1, in_focus_x0:in_focus_x1]
        sub_img = cv2.resize(sub_img, (int(real_x1 - real_x0), int(real_y1 - real_y0)))
        img[real_y0:real_y1, real_x0:real_x1] = sub_img 
    else: 
        print "NOT in zoom in mode!!!!!!!"
        img = out_focus[ylim[0]:ylim[1], xlim[0]:xlim[1]] 
        img = cv2.resize(img, (1024, 768)) 
    return img 
       
       
    def zoom_fun(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN or event == cv2.EVENT_MOUSEWHEEL:
            cur_xrange = (cur_xlim[1] - cur_xlim[0]) * 0.5
            cur_yrange = (cur_ylim[1] - cur_ylim[0]) * 0.5 
        # get x and y locations of the scroll event and the click event 
            if event == cv2.EVENT_MOUSEWHEEL: 
                if flags > 0:
                # deal with zoom in 
                    scale_factor = 1 / base_scale 
                elif flags < 0: 
                # deal with zoom out 
                    scale_factor = base_scale 
                else: 
                 # deal with something that should never happen 
                    scale_factor = 1 
            if event == cv2.EVENT_LBUTTONDOWN:
                if mode == 0:
                    scale_factor = 1 / base_scale
                elif mode == 1:
                    scale_factor = base_scale
                else:
                    scale_factor = 1
            cur_xlim = [xlow if xlow > -1 else 0,
                    xhigh if xhigh < xlim else xlim-1]
            cur_ylim = [ylow if ylow > -1 else 0, 
                    yhigh if yhigh < ylim else ylim-1] 
            if -0.1 <= ((cur_ylim[1] - cur_ylim[0]) / (cur_xlim[1] - cur_xlim[0]) - 3./4) <= 0.1: 
            #    if (cur_ylim[1] - cur_ylim[0]) < 200:
            #        curr_img = find_zoom_in_img(cur_xlim, cur_ylim, x, y)
            #    else:
            #        curr_img = out_focus[cur_ylim[0]:cur_ylim[1], cur_xlim[0]:cur_xlim[1]]                
            #        curr_img = cv2.resize(curr_img, (1024, 768)) 
                 curr_img = curr_node.generateView(x, y, cur_xlim, cur_ylim)
    return zoom_fun
       
       
def main():
    '''test some Jpeg Tree with user input'''
    '''at the same time, print the tree structure, and the current loaded tree''' 
    '''How jpeg is configured?'''# zoom in / out demo
    cv2.namedWindow("zoom")
    cv2.setMouseCallback("zoom", f)
    cv2.resizeWindow("zoom", 1024, 767)


    while True:
     #   if focus_now:
     #		out_focus_copy = out_focus.copy()
    
        key = cv2.waitKey(20)
    
        if key != -1:
            print key
        if key == 97: # 'a' -> zoom in 
            mode = 0
        if key == 115: # 's' -> zoom out 
            mode = 1 
#	if key == 97:
	    #if not in_focus_saved: # take pics 
	     #   # make dir
	#	    index = 2
	#	    makingDir(index)
	#	    cv2.imwrite('image_saved/pair' + str(index) + '/infocus.jpg', frame)
	#	    in_focus_saved = True
	 #   else:
		    # save the out of focus one 
		#	cv2.imwrite('image_saved/pair' + str(index) + '/outfocus.jpg', frame) 
#	if key == 115: # goes into interactive view mode
	    # TODO: firstly load the out of focus one 
		#       when clicked on a region, zoom in to that region, and replace the content with the focused one
		#       may display another "something" showing the result of blending the out of focus one with the in focus one 
#	    print "s pressed"
        if key == 27: # exit on ESC
            break
    cv2.destroyWindow("preview")

    
if __name__ == '__main__':
    main()    

        

# zoom in / out demo
import matplotlib.pyplot as plt
import cv2
import numpy as np

image_dir = 'image_saved/exp00/'

mm_25_00 = cv2.imread(image_dir + '25mm_00.ppm')
#mm_25_00_x = 206
#mm_25_00_y = 304
#mm_25_00_w = 325
#mm_25_00_h = 246 

mm_25_01 = cv2.imread(image_dir + '25mm_01.ppm')
mm_25_02 = cv2.imread(image_dir + '25mm_02.ppm')
mm_8_00 = cv2.imread(image_dir + '8mm_00.ppm') 

curr_img = mm_8_00.copy()
out_focus = mm_8_00.copy()
out_focus_copy = out_focus.copy()


cur_xlim = [0,curr_img.shape[1]]
cur_ylim = [0,curr_img.shape[0]]


xlim = out_focus.shape[1]
ylim = out_focus.shape[0]


# TODO: discover a blending approach 
mode = 0 # 0: zoom in, 1: zoom out


mm_25_00_x = 206 * 2 
mm_25_00_y = 304 * 2
mm_25_00_w = 325 * 2 
mm_25_00_h = 246 * 2 

ratio = 2048 / (325 * 2)#
#ratio2 = 1024  / (mm_25_00_w - mm_25_00_x)

def find_zoom_in_img(xlim, ylim, x, y): 
    img = None
    ratio2 = 1024  / (xlim[1] - xlim[0])

    x = x
    y = y
    if mm_25_00_x / 2 <= x <= mm_25_00_w / 2 + mm_25_00_x / 2 and mm_25_00_y /2  <= y <= mm_25_00_h / 2+ mm_25_00_y/ 2: 
        print "in zoom in mode!!!!!!!"
        # blend with the 25mm image 
        img = out_focus[ylim[0]:ylim[1], xlim[0]:xlim[1]]
        in_focus_x0 = xlim[0] if xlim[0] > mm_25_00_x else mm_25_00_x
        in_focus_x1 = xlim[1] if xlim[1] < mm_25_00_w + mm_25_00_x else mm_25_00_w + mm_25_00_x 
        in_focus_y0 = ylim[0] if ylim[0] > mm_25_00_y else mm_25_00_y
        in_focus_y1 = ylim[1] if ylim[1] < mm_25_00_h + mm_25_00_y else mm_25_00_h + mm_25_00_y
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

    else: 
        print "NOT in zoom in mode!!!!!!!"
        img = out_focus[ylim[0]:ylim[1], xlim[0]:xlim[1]] 
        img = cv2.resize(img, (1024, 768)) 
    return img 
     
      
def zoom_factory(base_scale = 2.):
    def zoom_fun(event, x, y, flags, param):
        global cur_xlim, cur_ylim, curr_img, out_focus
        if event == cv2.EVENT_LBUTTONDOWN or event == cv2.EVENT_MOUSEWHEEL:
            cur_xrange = (cur_xlim[1] - cur_xlim[0]) * 0.5  
            cur_yrange = (cur_ylim[1] - cur_ylim[0]) * 0.5 
        # get x and y locations of the scroll event 
            xdata = x * 2
            ydata = y * 2
          #  print param
        #    print flags
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
         #   print event.button 
        # set new limits 
            xlow = xdata - cur_xrange * scale_factor 
            xhigh = xdata + cur_xrange * scale_factor
            ylow = ydata - cur_yrange * scale_factor 
            yhigh = ydata + cur_yrange * scale_factor 
            cur_xlim = [xlow if xlow > -1 else 0,
                    xhigh if xhigh < xlim else xlim-1]
            cur_ylim = [ylow if ylow > -1 else 0, 
                    yhigh if yhigh < ylim else ylim-1] 
       #     print (cur_ylim[1] - cur_ylim[0]) / (cur_xlim[1] - cur_xlim[0]) - 3./4
            if -0.1 <= ((cur_ylim[1] - cur_ylim[0]) / (cur_xlim[1] - cur_xlim[0]) - 3./4) <= 0.1: 
                if (cur_ylim[1] - cur_ylim[0]) < 200:
                 #   curr_img = in_focus[cur_ylim[0]:cur_ylim[1], cur_xlim[0]:cur_xlim[1]]  
                    curr_img = find_zoom_in_img(cur_xlim, cur_ylim, x, y)
                else:
                    curr_img = out_focus[cur_ylim[0]:cur_ylim[1], cur_xlim[0]:cur_xlim[1]]                
                    curr_img = cv2.resize(curr_img, (1024, 768)) 
      #    ax.set_xlim([xdata - cur_xrange * scale_factor, 
    #                  xdata + cur_xrange * scale_factor])
    #    ax.set_ylim([ydata - cur_yrange * scale_factor, 
    #                 ydata + cur_yrange * scale_factor])
    #    plt.draw()
    return zoom_fun
    
#fig = plt.figure()
#ax = fig.add_subplot(211)
#ax.plot(range(10))
scale = 1.5 
f = zoom_factory(base_scale = scale)
cv2.namedWindow("zoom")
cv2.setMouseCallback("zoom", f)
cv2.resizeWindow("zoom", 1024, 767)

curr_img = cv2.resize(curr_img, (1024, 768)) 

while True:
 #   if focus_now:
 #		out_focus_copy = out_focus.copy()
    
    cv2.imshow("zoom", curr_img)

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


    
# zoom in / out demo
import matplotlib.pyplot as plt
import cv2
import numpy as np


index = 1
image_dir = 'image_saved/pair' + str(index) + '/'

out_focus = cv2.imread(image_dir + 'outfocus.jpg')
in_focus = cv2.imread(image_dir + 'infocus.jpg')
out_focus_copy = out_focus.copy()
curr_img = out_focus.copy()
cur_xlim = [0,curr_img.shape[1]]
cur_ylim = [0,curr_img.shape[0]]


xlim = out_focus.shape[1]
ylim = out_focus.shape[0]
# TODO: modify this to detect only mouse scroll events 
def zoom_factory(base_scale = 2.):
    def zoom_fun(event, x, y, flags, param):
        if event == cv2.EVENT_MOUSEWHEEL: 
        
            global cur_xlim, cur_ylim, curr_img, out_focus, in_focus
        # todo: change this based on image        
      #  cur_xlim = ax.get_xlim()
      #  cur_ylim = ax.get_ylim()
            cur_xrange = (cur_xlim[1] - cur_xlim[0]) * 0.5  
            cur_yrange = (cur_ylim[1] - cur_ylim[0]) * 0.5 
        # get x and y locations of the scroll event 
            xdata = x
            ydata = y 
            print param
            print flags
            if flags > 0:
            # deal with zoom in 
                scale_factor = 1 / base_scale 
            elif flags < 0: 
            # deal with zoom out 
                scale_factor = base_scale 
            else: 
             # deal with something that should never happen 
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
            print (cur_ylim[1] - cur_ylim[0]) / (cur_xlim[1] - cur_xlim[0]) - 3./4
            if -0.1 <= ((cur_ylim[1] - cur_ylim[0]) / (cur_xlim[1] - cur_xlim[0]) - 3./4) <= 0.1: 
                if (cur_ylim[1] - cur_ylim[0]) < 200:
                    curr_img = in_focus[cur_ylim[0]:cur_ylim[1], cur_xlim[0]:cur_xlim[1]]  
                else:
                    curr_img = out_focus[cur_ylim[0]:cur_ylim[1], cur_xlim[0]:cur_xlim[1]]                
                curr_img = cv2.resize(curr_img, (1024, 768)) 
      #    ax.set_xlim([xdata - cur_xrange * scale_factor, 
    #                  xdata + cur_xrange * scale_factor])
    #    ax.set_ylim([ydata - cur_yrange * scale_factor, 
    #                 ydata + cur_yrange * scale_factor])
    #    plt.draw()
       
  #  fig = ax.get_figure()
    # TODO change this
    
  #  fig.canvas.mpl_connect('scroll_event', zoom_fun)   
    return zoom_fun
    
#fig = plt.figure()
#ax = fig.add_subplot(211)
#ax.plot(range(10))
scale = 1.5 
f = zoom_factory(base_scale = scale)
cv2.namedWindow("zoom")
cv2.setMouseCallback("zoom", f)

while True:
 #   if focus_now:
 #		out_focus_copy = out_focus.copy()
    cv2.imshow("zoom", curr_img)
    key = cv2.waitKey(20)
   # if key != -1:
    #    print key
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


    
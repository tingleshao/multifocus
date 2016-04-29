import matplotlib.pyplot as plt
import cv2
import numpy as np
import time


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


class JPEGTreeNavigator: 
    def f(self):
        return 'hello world!'
         
    def __init__(self, starting_node):
        self.curr_node = starting_node
        self.prev_node = None
        self.in_layer2 = False
        
    def printCurrNodeInfo(self):
        curr_node_name = self.curr_node.getName() if self.curr_node else "none"
        prev_node_name = self.prev_node.getName() if self.prev_node else "none"
        print "curr node: " + curr_node_name + "; parent node: " + prev_node_name
        
    def imageEnhancement(self): 
    # enhance the image when zoomed in 
        return None
        
    def generateView(self, x, y, curr_xlim, curr_ylim):
    # responsible for triversing the tree
        img = None
        
        xlim = curr_xlim
        ylim = curr_ylim 
        ratio2 = 1024 / (xlim[1] - xlim[0])
        if (curr_ylim[1] - curr_ylim[0] < 200):
            # node should not have generateView() 
            # approach: having a reference to the current mom node, and blend using the mom node data and current data 
            if not self.in_layer2:
                self.prev_node = self.curr_node 
            # where can we get mm_25_00_xxx? => it is global. 
            if mm_25_00_x / 2 <= x <= mm_25_w / 2 + mm_25_00_x / 2 and mm_25_00_y / 2 <= y <= mm_25_h / 2 + mm_25_00_y / 2: 
                if not self.in_layer2:
                    self.curr_node = self.curr_node.getChild(0)
                print "in zoom mode 0!w"
                child_img = self.curr_node.data 
                img = self.prev_node.data[ylim[0]:ylim[1], xlim[0]:xlim[1]]
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
                sub_img = child_img[in_focus_y0:in_focus_y1, in_focus_x0:in_focus_x1]
                sub_img = cv2.resize(sub_img, (int(real_x1 - real_x0), int(real_y1 - real_y0)))
                img[real_y0:real_y1, real_x0:real_x1] = sub_img 
            elif mm_25_01_x / 2 <= x <= mm_25_w / 2 + mm_25_01_x / 2 and mm_25_01_y / 2 <= y <= mm_25_h / 2 + mm_25_01_y / 2:
                if not self.in_layer2:
                    self.curr_node = self.curr_node.getChild(1)
                print "in zoom mode 1!w"
                child_img = self.curr_node.data 
                img = self.prev_node.data[ylim[0]:ylim[1], xlim[0]:xlim[1]]
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
                sub_img = child_img[in_focus_y0:in_focus_y1, in_focus_x0:in_focus_x1]
                sub_img = cv2.resize(sub_img, (int(real_x1 - real_x0), int(real_y1 - real_y0)))
                img[real_y0:real_y1, real_x0:real_x1] = sub_img 
            elif mm_25_02_x / 2 <= x <= mm_25_w / 2 + mm_25_02_x / 2 and mm_25_02_y / 2 <= y <= mm_25_h / 2 + mm_25_02_y / 2:
                if not self.in_layer2:
                    self.curr_node = self.curr_node.getChild(2)
                print "in zoom mode 2!w"
                child_img = self.curr_node.data 
                img = self.prev_node.data[ylim[0]:ylim[1], xlim[0]:xlim[1]]
                in_focus_x0 = xlim[0] if xlim[0] > mm_25_02_x else mm_25_02_x 
                in_focus_x1 = xlim[1] if xlim[1] < mm_25_w + mm_25_02_x else mm_25_w + mm_25_02_x 
                in_focus_y0 = ylim[0] if ylim[0] > mm_25_02_y else mm_25_02_y
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
                sub_img = child_img[in_focus_y0:in_focus_y1, in_focus_x0:in_focus_x1]
                sub_img = cv2.resize(sub_img, (int(real_x1 - real_x0), int(real_y1 - real_y0)))
                img[real_y0:real_y1, real_x0:real_x1] = sub_img 
            else: 
            # can we ever get here? 
                 print "NOT in zoom in mode!!!!!!!"
                 img = out_focus[ylim[0]:ylim[1], xlim[0]:xlim[1]] 
                 img = cv2.resize(img, (1024, 768))             
         #   img = self.curr_node.generateView(x, y, curr_xlim, curr_ylim)
            self.in_layer2 = True
        else: 
            if self.curr_node.getMom():
                self.curr_node = self.curr_node.getMom()
                self.prev_node = None
                self.in_layer2 = False
            img = self.curr_node.data[curr_ylim[0]:curr_ylim[1], curr_xlim[0]:curr_xlim[1]]
        return cv2.resize(img, (1024, 768))
        

class JPEGNode:
    def f(self): 
        return 'hello world'
     
    def __init__(self, data, children, mom, upper_x, upper_y, w, h, name): 
        self.data = data 
        self.children = children 
        self.mom = mom
        self.upper_x = upper_x  
        self.upper_y = upper_y 
        self.w = w 
        self.h = h   
        self.xlim = data.shape[1]
        self.ylim = data.shape[0]
        self.name = name

    def setMom(self, mom):
        self.mom = mom
     
    def getMom(self):
        return self.mom
        
    def getName(self):
        return self.name
     
    def getChild(self, index):
    # later change this by having a map between x, y and child id 
    # so that we can have multiple children returned.
        return self.children[index]
          
    # TODO: discover a blending approach 
  #  def generateView(self, x, y, curr_xlim, curr_ylim):
  #     #    if (cur_ylim[1] - cur_ylim[0]) < 200:
  #          #        curr_img = find_zoom_in_img(cur_xlim, cur_ylim, x, y)
            #    else:
            #        curr_img = out_focus[cur_ylim[0]:cur_ylim[1], cur_xlim[0]:cur_xlim[1]]                
            #        curr_img = cv2.resize(curr_img, (1024, 768)) 
   #     if (curr_ylim[1] - curr_ylim[0]) < 200: 
   #         img = self.find_zoom_in_img(curr_xlim, curr_ylim, x, y)
  #      else: 
   #         img =  self.data[curr_ylim[0]:curr_ylim[1], curr_xlim[0]:curr_xlim[1]]
   #     return img
        
mm_25_00_t = JPEGNode(mm_25_00, [], None, mm_25_00_x, mm_25_00_y, mm_25_w, mm_25_h, "25 mm 00")
mm_25_01_t = JPEGNode(mm_25_01, [], None, mm_25_01_x, mm_25_01_y, mm_25_w, mm_25_h, "25 mm 01")
mm_25_02_t = JPEGNode(mm_25_02, [], None,mm_25_02_x, mm_25_02_y, mm_25_w, mm_25_h, "25 mm 02")
mm_8_00_t = JPEGNode(mm_8_00, [mm_25_00_t, mm_25_01_t, mm_25_02_t], None, 0, 0, mm_8_w, mm_8_h, "8 mm 00")

mm_25_00_t.setMom(mm_8_00_t)
mm_25_01_t.setMom(mm_8_00_t)
mm_25_02_t.setMom(mm_8_00_t)

nav = JPEGTreeNavigator(mm_8_00_t)
curr_img = mm_8_00.copy()
#curr_node = m_8_00_t

out_focus = mm_8_00.copy()
out_focus_copy = out_focus.copy()

cur_xlim = [0,mm_8_w]
cur_ylim = [0,mm_8_h]
xlim = out_focus.shape[1]
ylim = out_focus.shape[0]

mode = 0 # 0: zoom in, 1: zoom out

ratio = 2048 / (325 * 2)
scale = 1.5 
       
def zoom_tree_factory(base_scale = 2.):
    def zoom_fun(event, x, y, flags, param):
        global cur_xlim, cur_ylim, nav, curr_img
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
            xlow = x*2 - cur_xrange * scale_factor 
            xhigh = x*2 + cur_xrange * scale_factor
            ylow = y*2 - cur_yrange * scale_factor 
            yhigh = y*2 + cur_yrange * scale_factor 
            cur_xlim = [xlow if xlow > -1 else 0,
                    xhigh if xhigh < xlim else xlim-1]
            cur_ylim = [ylow if ylow > -1 else 0, 
                    yhigh if yhigh < ylim else ylim-1] 
            if -0.1 <= ((cur_ylim[1] - cur_ylim[0]) / (cur_xlim[1] - cur_xlim[0]) - 3./4) <= 0.1: 
                curr_img = nav.generateView(x, y, cur_xlim, cur_ylim) # current node is responsible for generating a view.
                nav.printCurrNodeInfo()
    return zoom_fun
       
       
def main():
    global cur_xlim, cur_ylim, curr_img
    '''test some Jpeg Tree with user input'''
    '''at the same time, print the tree structure, and the current loaded tree''' 
    '''How jpeg is configured?'''# zoom in / out demo
    # zoom_tree_factory is for detecting mouse events 
    f = zoom_tree_factory(base_scale = scale)
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
            print "mode swtiched to zoom in"
        if key == 115: # 's' -> zoom out 
            mode = 1 
            print "mode switched to zoom out"
        if key == 119:
            print "take streen shot: " + str(time.time()).split('.')[0] + '.png'
            cv2.imwrite(str(time.time()).split('.')[0] + '.png', curr_img)
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

        

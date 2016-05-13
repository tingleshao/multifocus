import numpy as np
import cv2
import imutils
import time
import matplotlib.pyplot as plt
from stitcher import Stitcher


class TreeNavigator:          
    def __init__(self, starting_node):
        print 'navigator init...'
        self.curr_node = starting_node
        self.global_frame = starting_node.getFrame()
        self.prev_node = None
        self.in_layer2 = False
        self.H = None

    def setH(self, H):
        self.H = H 
        
    def printCurrNodeInfo(self):
        curr_node_name = self.curr_node.getName() if self.curr_node else "none"
        prev_node_name = self.prev_node.getName() if self.prev_node else "none"
        print "curr node: " + curr_node_name + "; parent node: " + prev_node_name
        
    def imageEnhancement(self): 
    # enhance the image when zoomed in 
        return None
        
    def generateOverview(self, x, y, curr_xlim, curr_ylim): 
        print "overview changed!"
    # generate the small window showing the overview: where I am with respect to the global
        img = self.global_frame
        img = cv2.resize(img, (500, 357)) 
        img = cv2.warpPerspective(img, self.H, (img.shape[1] + img.shape[1], img.shape[0] + img.shape[1]))
        cv2.rectangle(img,(int(curr_xlim[0]*1000./3840), int(curr_ylim[0]*1000./3840)),(int(cur_xlim[1]*1000./3840), int(curr_ylim[1]*1000./3840)),(0,255,0),3)
        img = cv2.resize(img, (500, 357))
        return img
  
    def generateView(self, x, y, curr_xlim, curr_ylim):
    # curr_xlim / curr_ylim: x - y lims in global space
    # responsible for triversing the tree
        img = None
        ratio2 = 500. / (curr_xlim[1] - curr_xlim[0])
        ratio1 = 500. / 3840
        if (curr_ylim[1] - curr_ylim[0] < 500):
            # approach: having a reference to the current mom node, and blend using the mom node data and current data 
            if not self.in_layer2:
                # enter layer 2
                if 0 < transformX(x) < 3840 / 2 or 0 < transformX(y) < 2748 / 2:
                    self.prev_node = self.curr_node  
                    self.curr_node = self.curr_node.getChild(0)
                    print "enter in zoom in mode"
                    child_img = self.curr_node.getFrame() 
                    img = self.prev_node.getFrame()
                    img = cv2.resize(img, (500, 357))
                    img = cv2.warpPerspective(img, self.H, (img.shape[1] + img.shape[1], img.shape[0] + img.shape[1]))
                    img = img[curr_ylim[0] * 1000./3840:curr_ylim[1]* 1000./3840, curr_xlim[0]* 1000./3840:curr_xlim[1]* 1000./3840]
                    in_focus_x0 = curr_xlim[0] * 2 if curr_xlim[0] > 0 else 0
                    in_focus_x1 = curr_xlim[1] * 2 if curr_xlim[1] < 3840 / 2 + 0 else 3840 + 0 
                    in_focus_y0 = curr_ylim[0] * 2 if curr_ylim[0] > 0 else 0
                    in_focus_y1 = curr_ylim[1] * 2 if curr_ylim[1] < 2748 / 2 + 0 else 2748 + 0  
                    # test if in_focus is computed correctly
                    child_img_small = cv2.resize(child_img, (500, 357)) 
                    cv2.rectangle(child_img_small, (int(in_focus_x0 * 500. / 3840), int(in_focus_y0 * 500. / 3840)), (int(in_focus_x1*500./3840), int(in_focus_y1*500./3840)), (0,255,0), 3)

                    real_x0 = ((in_focus_x0)/2 - curr_xlim[0]) * ratio2 
                    real_x1 = ((in_focus_x1)/2 - curr_xlim[0]) * ratio2
                    real_y0 = ((in_focus_y0)/2 - curr_ylim[0]) * ratio2
                    real_y1 = ((in_focus_y1)/2 - curr_ylim[0]) * ratio2  
                    real_x0 = real_x0 if real_x0 > 0 else 0
                    real_x1 = real_x1 if real_x1 < 500 else 500
                    real_y0 = real_y0 if real_y0 > 0 else 0
                    real_y1 = real_y1 if real_y1 < 357 else 357
                    
                    cv2.imshow("test", child_img_small)

                    img = cv2.resize(img, (500, 357))
                    cv2.rectangle(img, (int(real_x0), int(real_y0)), (int(real_x1), int(real_y1)), (255,0,0),3)
                    cv2.imshow("test2", img)
 
                    print "in focus: " + str(in_focus_y0) + " " + str(in_focus_y1) + " " + str(in_focus_x0) + " " + str(in_focus_x1)  
                    print "real: " + str(real_y0) + " " + str(real_y1) + " " + str(real_x0) + " " + str(real_x1)
                    print "img: " + str(img.shape)
                    sub_img = child_img[in_focus_y0:in_focus_y1, in_focus_x0:in_focus_x1]
                    sub_img = cv2.resize(sub_img, (int(real_x1) - int(real_x0), int(real_y1) - int(real_y0)))
                    img[int(real_y0):int(real_y1), int(real_x0):int(real_x1)] = sub_img 
            else: 
                 print "stay in curr node mode!!!!!!!"
                 img = self.curr_node.getFrame()
                 img = img[int(curr_ylim[0])*2:int(curr_ylim[1])*2, int(curr_xlim[0])*2:int(curr_xlim[1])*2] 
                 img = cv2.resize(img, (500, 357))             
         #   img = self.curr_node.generateView(x, y, curr_xlim, curr_ylim)
            self.in_layer2 = True
        else: 
            print "in out mode!"
            if self.curr_node.getMom():
                self.curr_node = self.curr_node.getMom()
                self.prev_node = None
                self.in_layer2 = False
            img = self.curr_node.getFrame()
            img = cv2.resize(img, (500, 357)) 
            img1 = cv2.warpPerspective(img, self.H, (img.shape[1] + img.shape[1], img.shape[0] + img.shape[0]))
            img1 = img1[curr_ylim[0] * 1000./3840:curr_ylim[1] * 1000./3840, curr_xlim[0] * 1000./3840:curr_xlim[1] * 1000./3840]
            img = img1
        return cv2.resize(img, (500, 357))
        

class TreeNode:
    def __init__(self, data, children, mom, upper_x, upper_y, w, h, name): 
        print 'Node init...'
        self.data = data 
        self.children = children 
        self.mom = mom
        self.upper_x = upper_x  
        self.upper_y = upper_y 
        self.w = w 
        self.h = h   
        self.xlim = 3840
        self.ylim = 2748
        self.name = name
        self.frame_counter = 0 

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
    
    def getFrame(self):
        ret, frame = self.data.read()
   #     frame = cv2.resize(frame, (500, 357))
        self.frame_counter += 1
        if self.frame_counter == self.data.get(cv2.CAP_PROP_FRAME_COUNT)-1:
            self.frame_counter = 0
            self.data.set(cv2.CAP_PROP_POS_FRAMES, 0)
        return frame    
              

#image_dir = 'image_saved/exp00/'

v0 = cv2.VideoCapture('/home/chong/Data/acA3800-14uc__21833705__20160422_141738868.avi')
v1 = cv2.VideoCapture('/home/chong/Data/acA3800-14uc__21833709__20160422_141618171.avi') 
v0.get(cv2.CAP_PROP_FPS)

mm_00_w = 3840
mm_00_h = 2748 

mm_01_w = 3840
mm_01_h = 2748

mm_00_x = 3840 
mm_00_y = 2748

mm_01_x = 3840
mm_01_y = 2748 
        
mm_01_t = TreeNode(v1, [], None, mm_01_x, mm_01_y, mm_01_w, mm_01_h, "video 01")        
mm_00_t = TreeNode(v0, [mm_01_t], None, mm_00_x, mm_00_y, mm_00_w, mm_00_h, "video 00")

cur_xlim = [0, mm_00_w]
cur_ylim = [0, mm_00_h]
H = np.array([[1.99116709e+00, 2.96239415e-02, 4.03929046e+01], [ -8.01318987e-02, 2.10573123e+00, 3.05521944e+01], [-1.99180445e-04, 4.62456395e-05, 1.00000000e+00]])
curr_img = mm_00_t.getFrame()
overview_img = mm_00_t.getFrame()
curr_img = cv2.resize(curr_img, (500, 357))
curr_img = cv2.warpPerspective(curr_img, H, (curr_img.shape[1] + curr_img.shape[1], curr_img.shape[0] + curr_img.shape[0]))
overview_img = cv2.resize(overview_img, (500, 357))
overview_img = cv2.warpPerspective(overview_img, H, (overview_img.shape[1] + overview_img.shape[1], overview_img.shape[0] + overview_img.shape[0]))
#print curr_img
mm_01_t.setMom(mm_00_t)

nav = TreeNavigator(mm_00_t)

xlim = 3840
ylim = 2748

mode = 0 # 0: zoom in, 1: zoom out

ratio = 3840 / (500 * 2)
scale = 1.5 

# H: [[  1.99116709e+00   2.96239415e-02   4.03929046e+01]
# [ -8.01318987e-02   2.10573123e+00   3.05521944e+01]
# [ -1.99180445e-04   4.62456395e-05   1.00000000e+00]]

def transformX(x):
    return int(float(x) * 3840 / 500)

       
def zoom_tree_factory(base_scale = 2.):
    def zoom_fun(event, x, y, flags, param):
        global cur_xlim, cur_ylim, nav, curr_img, overview_img
        if event == cv2.EVENT_LBUTTONDOWN or event == cv2.EVENT_MOUSEWHEEL:
            print "L button down!" 
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
                    print 1
                    print x, y, cur_xlim, cur_ylim
                    scale_factor = 1 / base_scale
                elif mode == 1:
                    print 2
                    scale_factor = base_scale
                else:
                    print 3
                    scale_factor = 1
            xlow = transformX(x) - cur_xrange * scale_factor 
            xhigh = transformX(x) + cur_xrange * scale_factor
            ylow = transformX(y) - cur_yrange * scale_factor 
            yhigh = transformX(y) + cur_yrange * scale_factor 
            cur_xlim = [xlow if xlow > -1 else 0,
                    xhigh if xhigh < xlim else xlim-1]
            cur_ylim = [ylow if ylow > -1 else 0, 
                    yhigh if yhigh < ylim else ylim-1]        
            if -0.1 <= ((cur_ylim[1] - cur_ylim[0]) / (cur_xlim[1] - cur_xlim[0]) - 2748./3840) <= 0.1: 
                curr_img = nav.generateView(x, y, cur_xlim, cur_ylim) 
                overview_img = nav.generateOverview(x, y, cur_xlim, cur_ylim)
                nav.printCurrNodeInfo()
    return zoom_fun


def main():
    global curr_img, overview_img, nav
    cap0 = cv2.VideoCapture('/home/chong/Data/acA3800-14uc__21833705__20160422_141738868.avi')
    cap1 = cv2.VideoCapture('/home/chong/Data/acA3800-14uc__21833709__20160422_141618171.avi') 
    fps = cap0.get(cv2.CAP_PROP_FPS)

    frame_counter = 0 

    first_frame0 = None
    first_frame1 = None
    # TODO: show a subwindow
    # TODO: frame rate is limited by how fast the library can render the frame (reading frame from disk and display it on the screen)
    #       right now this is only relevant to the opencv video read code
    # TODO: tree data structure
    # TODO: go some deep shit: H.265 multi scale support investigate in x265.s
    # TODO: click zoom in 
    # TODO: code for switching neighbor view, etc.
    # TODO: discover a blending approach 

    stitched = True
    H = np.array([[1.99116709e+00, 2.96239415e-02, 4.03929046e+01], [ -8.01318987e-02, 2.10573123e+00, 3.05521944e+01], [-1.99180445e-04, 4.62456395e-05, 1.00000000e+00]])
    nav.setH(H)

#    global cur_xlim, cur_ylim, curr_img
    '''test some Jpeg Tree with user input'''
    '''at the same time, print the tree structure, and the current loaded tree''' 
    '''How jpeg is configured?'''# zoom in / out demo
    # zoom_tree_factory is for detecting mouse events 
    f = zoom_tree_factory(base_scale = scale)
    cv2.namedWindow("zoom")
    cv2.setMouseCallback("zoom", f)
    cv2.resizeWindow("zoom", 500, 357)
    print "\n\n\n\n\n"
    print curr_img
    print "\n\n\nwww\n\n\n"
   # x = np.array(curr_img)
    curr_img = cv2.resize(curr_img, (500, 357)) 
    overview_img = cv2.resize(overview_img, (500, 357))
    while True:
      #  if focus_now:
#     		out_focus_copy = out_focus.copy()
        #curr_img = nav.generateView()
        cv2.imshow("zoom", curr_img)
        cv2.imshow("overview", overview_img)
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
        if key == 27: # exit on ESC
            break
    cv2.destroyWindow("preview")

    while True:
        ret, frame0 = cap0.read()
        frame0 = cv2.resize(frame0, (500, 357))
        if (first_frame1 == None) and (frame_counter == 0):
            first_frame1 = frame0
        ret, frame1 = cap1.read()
        frame1 = cv2.resize(frame1, (500, 357))
        if (first_frame0 == None) and (frame_counter == 0): 
            first_frame0 = frame1 

        if not stitched:
            stitched = True
            first_frame0 = imutils.resize(first_frame0, width=500)
            first_frame1 = imutils.resize(first_frame1, width=500)
            stitcher = Stitcher()
            (result, vis, H) = stitcher.stitch([first_frame0, first_frame1], showMatches=True)
          #  H = np.array([[1.99116709e+00, 2.96239415e-02, 4.03929046e+01], [ -8.01318987e-02, 2.10573123e+00, 3.05521944e+01], [-1.99180445e-04, 4.62456395e-05, 1.00000000e+00]])
            print "H: " + str(H)
            cv2.imshow("image A", first_frame0)
            cv2.imshow("image B", first_frame1) 
            cv2.imshow("Keypoint Matches", vis) 
            cv2.imshow("Result", result)      
    
        if H != None:
            wframe0 = cv2.warpPerspective(frame0, H, (frame0.shape[1] + frame1.shape[1], frame0.shape[0] + frame1.shape[0]))
            
        m,n = frame1.shape[:2]
        cv2.putText(frame0, "frame: " + str(frame_counter) + " fps: " + str(fps), (5, m-5),  cv2.FONT_HERSHEY_PLAIN, fontScale=1.0, color=(255,255,255), thickness=1)
        cv2.putText(frame1, "frame: " + str(frame_counter), (5, m-5),  cv2.FONT_HERSHEY_PLAIN, fontScale=1.0, color=(255,255,255), thickness=1)
        frame_counter += 1
      # because the video recording is terminated due to file size issue, the last frame has a problem, we cannot reach it otherwise it will break
        if frame_counter == cap0.get(cv2.CAP_PROP_FRAME_COUNT)-1 or frame_counter == cap1.get(cv2.CAP_PROP_FRAME_COUNT) -1:
            frame_counter = 0
            cap0.set(cv2.CAP_PROP_POS_FRAMES, 0)
            cap1.set(cv2.CAP_PROP_POS_FRAMES, 0)
        gray0 = cv2.cvtColor(frame0, cv2.COLOR_BGR2GRAY)
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY) 
        cv2.imshow('frame0', gray0)
        cv2.imshow('frame1', gray1) 
        cv2.imshow('warped frame0', wframe0)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap0.release()
    cap1.release()
    cv2.destroyAllWindows()

    
if __name__ == '__main__':
    main()    


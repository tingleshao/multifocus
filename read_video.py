import numpy as np
import cv2
import imutils



class Stitcher: 
    def __init__(self):
        self.isv3 = imutils.is_cv3()

    def stitch(self, images, ratio=0.75, reprojThresh=4.0, showMatches=False):
        (imageB, imageA) = images 
        (kpsA, featuresA) = self.detectAndDescribe(imageA)
        (kpsB, featuresB) = self.detectAndDescribe(imageB) 
  
        M = self.matchKeypoints(kpsA, kpsB, featuresA, featuresB, ratio, reprojThresh) 
    
        if M is None:
            return None

        (matches, H, status) = M 
        result = cv2.warpPerspective(imageA, H, (imageA.shape[1] + imageB.shape[1], imageA.shape[0]))
        result[0:imageB.shape[0], 0:imageB.shape[1]] = imageB
        if showMatches:
            vis = self.drawMatches(imageA, imageB, kpsA, kpsB, matches, status) 
            return (result, vis) 
        return result 
 

    def detectAndDescribe(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  
        if self.isv3:
            descriptor = cv2.xfeatures2d.SIFT_create() 
            (kps, features) = descriptor.detectAndCompute(image, None)
        else:
            detector = cv2.FeatureDetector_create("SIFT")
            kps = detetor.detect(gray) 
            extractor = cv2.DescriptorExtractor_create("SIFT")
            (kps, features) = extractor.compute(gray, kps)

        kps = np.float32([kp.pt for kp in kps])
        return (kps, features) 


    def matchKeypoints(self, kpsA, kpsB, featuresA, featuresB, ratio, reprojThresh):
        matcher = cv2.DescriptorMatcher_create("BruteForce")
        rawMatches = matcher.knnMatch(featuresA, featuresB, 2)
        matches = [] 
        for m in rawMatches:
            if len(m) == 2 and m[0].distance < m[1].distance * ratio:
                matches.append((m[0].trainIdx, m[0].queryIdx)) 
        if len(matches) > 4: 
            ptsA = np.float32([kpsA[i] for (_, i) in matches])
            ptsB = np.float32([kpsB[i] for (i, _) in matches]) 
    
            (H, status) = cv2.findHomography(ptsA, ptsB, cv2.RANSAC, reprojThresh) 
            return (matches, H, status) 
        return None 
  
     
    def drawMatches(self, imageA, imageB, kpsA, kpsB, matches, status): 
        (hA, wA) = imageA.shape[:2] 
        (hB, wB) = imageB.shape[:2] 
        vis = np.zeros((max(hA, hB), wA + wB, 3), dtype="uint8")
        vis[0:hA, 0:wA] = imageA
        vis[0:hB, wA:] = imageB
   
        for ((trainIdx, queryIdx), s) in zip(matches, status): 
            if s == 1:
                ptA = (int(kpsA[queryIdx][0]), int(kpsA[queryIdx][1]))
                ptB = (int(kpsB[trainIdx][0]) + wA, int(kpsB[trainIdx][1]))
                cv2.line(vis, ptA, ptB, (0, 255, 0), 1)
   
        return vis 


cap0 = cv2.VideoCapture('/home/chong/Data/acA3800-14uc__21833705__20160422_141738868.avi')
cap1 = cv2.VideoCapture('/home/chong/Data/acA3800-14uc__21833709__20160422_141618171.avi') 

frame_counter = 0 

first_frame0 = None
first_frame1 = None



'''import cv2
if __name__ == '__main__' :
 
    video = cv2.VideoCapture("video.mp4");
     
    # Find OpenCV version
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
     
    if int(major_ver)  < 3 :
        fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
        print "Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps)
    else :
        fps = video.get(cv2.CAP_PROP_FPS)
        print "Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps)
     
   video.release(); 
'''


# TODO measurement: bandwidth utilization, etc. 
# TODO: go some deep shit: tree data sturcture\
# TODO: go some deep shit: H.265 multi scale support investigate in x265.s

stitched = False

while True:
  #  while(cap.isOpened()):
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
        (result, vis) = stitcher.stitch([first_frame0, first_frame1], showMatches=True)
      
        cv2.imshow("image A", first_frame0)
        cv2.imshow("image B", first_frame1) 
        cv2.imshow("Keypoint Matches", vis) 
        cv2.imshow("Result", result)      
  

    m,n = frame1.shape[:2]
    cv2.putText(frame0, "frame: " + str(frame_counter), (5, m-5),  cv2.FONT_HERSHEY_PLAIN, fontScale=1.0, color=(255,255,255), thickness=1)
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
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap0.release()
cap1.release()
cv2.destroyAllWindows()


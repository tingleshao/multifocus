import numpy as np
import cv2

cap0 = cv2.VideoCapture('/home/chong/Data/acA3800-14uc__21833705__20160422_141738868.avi')
cap1 = cv2.VideoCapture('/home/chong/Data/acA3800-14uc__21833709__20160422_141618171.avi') 

frame_counter = 0 

# TODO stitich them 
# TODO measurement: framerate, bandwidth utilization, etc. 
# TODO: go some deep shit: tree data sturcture\
# TODO: go some deep shit: H.265 multi scale support investigate in x265.


while True:
  #  while(cap.isOpened()):
    ret, frame0 = cap0.read()
    frame0 = cv2.resize(frame0, (500, 378))
    ret, frame1 = cap1.read()
    frame1 = cv2.resize(frame1, (500, 378))
    m,n = frame1.shape[:2]
    cv2.putText(frame0, "frame: " + str(frame_counter), (5, m-5),  cv2.FONT_HERSHEY_PLAIN, fontScale=1.0, color=(255,255,255), thickness=1)
    cv2.putText(frame1, "frame: " + str(frame_counter), (5, m-5),  cv2.FONT_HERSHEY_PLAIN, fontScale=1.0, color=(255,255,255), thickness=1)
    #print frame_counter
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


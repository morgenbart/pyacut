# From https://www.geeksforgeeks.org/webcam-motion-detector-python/ on 2020-12-22.
# Python program to implement  
# Webcam Motion Detector 
  
# importing OpenCV, time and Pandas library 
import cv2, time, pandas, sys 
# importing datetime class from datetime library 
from datetime import datetime
  
# Assigning our static_back to None 
static_back = None
static_back_b = None
  
# List when any moving object appear 
motion_list = [] 
  
# Capturing video 
video = cv2.VideoCapture(sys.argv[1]) 
fpsr = int(video.get(cv2.CAP_PROP_FPS))
print(fpsr)

def resize(img, scale_percent):
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    return cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

framecount = 0  
previous_motion_state = 0
begintime=datetime.now()
# Infinite while loop to treat stack of image as video 
while True: 
    # Reading frame(image) from video 
    check, frame = video.read() 
    if not check:
        break

    framecount += 1 
  
    # Initializing motion = 0(no motion) 
    motion = 0
  
    # Converting color image to gray_scale image 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
  
    # Converting gray scale image to GaussianBlur  
    # so that change can be find easily 
    gray = cv2.GaussianBlur(gray, (21, 21), 0) 
  
    # In first iteration we assign the value  
    # of static_back to our first frame 
    if static_back is None:
        static_back = gray 

    # Difference between static background  
    # and current frame(which is GaussianBlur) 
    diff_frame = cv2.absdiff(static_back, gray) 
  
    # If change in between static background and 
    # current frame is greater than 30 it will show white color(255) 
    thresh_frame = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)[1] 
    thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2) 
  
    # Finding contour of moving object 
    cnts,_ = cv2.findContours(thresh_frame.copy(),  
                       cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
  
    for contour in cnts: 
        if cv2.contourArea(contour) < 2000: 
            continue
        motion = 1
  
        (x, y, w, h) = cv2.boundingRect(contour) 
        # making green rectangle arround the moving object 
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3) 
  
    
    if motion != previous_motion_state:
        print(f"motion state changed from {previous_motion_state} to"
                f" {motion} at own frame count {framecount}, timecount {video.get(cv2.CAP_PROP_POS_MSEC)}, framecount {video.get(cv2.CAP_PROP_POS_FRAMES)}, from begin {datetime.now() - begintime}.")
        previous_motion_state = motion
        if motion == 1:
            motion_list.append((framecount,))
        else:
            x = motion_list.pop()
            motion_list.append((x[0], framecount))

    if framecount % fpsr == 0:
        if static_back_b is None:
            static_back = gray
            static_back_b = gray
        else:
            static_back = static_back_b
            static_back_b = gray
  
    # Displaying image in gray_scale 
    #cv2.imshow("g", resize(static_back, 25)) 
    # Displaying the difference in currentframe to 
    # the staticframe(very first_frame) 
    #cv2.imshow("d", resize(diff_frame, 25)) 
    # Displaying the black and white image in which if 
    # intensity difference greater than 30 it will appear white 
    #cv2.imshow("t", resize(thresh_frame, 25)) 
    # Displaying color frame with contour of motion of object 
    cv2.imshow("c", resize(frame, 25)) 
    #cv2.moveWindow("g", 0, 0)
    #cv2.moveWindow("d", 300, 0)
    #cv2.moveWindow("t", 700, 0)
    cv2.moveWindow("c", 0, 400)

    key = cv2.waitKey(1) 
    # if q entered whole process will stop 
    if key == ord('q'): 
        # if something is movingthen it append the end time of movement 
        break

print(motion_list)
print(framecount)
  
video.release() 
# Destroying all the windows 
cv2.destroyAllWindows() 


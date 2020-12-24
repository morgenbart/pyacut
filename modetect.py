# From https://www.geeksforgeeks.org/webcam-motion-detector-python/ on 2020-12-22.
# Python program to implement  
# Webcam Motion Detector 
  
# importing OpenCV, time and Pandas library 
import cv2, os, time, pandas, sys 
# importing datetime class from datetime library 
from datetime import datetime

show_image = False
  
# Assigning our static_back to None 
static_back = None
static_back_b = None
  
# List when any moving object appear 
motion_list = [] 
  
# Capturing video 
clipname=sys.argv[1]
video = cv2.VideoCapture(clipname) 
fps = video.get(cv2.CAP_PROP_FPS)
fpsr = int(round(fps))
print(f"fps {fps}, rounded {fpsr}.")

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
  
    
    timecount = video.get(cv2.CAP_PROP_POS_MSEC)
    if motion != previous_motion_state:
        print(f"At {datetime.now() - begintime}.motion state changed from "
              f"{previous_motion_state} to  {motion} own frame count "
              f"{framecount}, timecount {timecount}, framecount "
              f"{video.get(cv2.CAP_PROP_POS_FRAMES)}.")
        previous_motion_state = motion
        if len(motion_list) == 0:
            motion_list.append((0, ))
        m = motion_list.pop()
        if motion == 1:
            if len(m) == 1:
                if (timecount - m[0] < 1000):
                    motion_list.append(m)
                else:
                    motion_list.append((timecount, ))
            else:
                if (timecount - m[1] < 1000):
                    motion_list.append((m[0], ))
                else:
                    motion_list.append(m)
                    motion_list.append((timecount, ))

        else:
            if (timecount - m[0] > 1000):
                motion_list.append((m[0], timecount))
        print(motion_list)

    if framecount % fpsr == 0:
        if static_back_b is None:
            static_back = gray
            static_back_b = gray
        else:
            static_back = static_back_b
            static_back_b = gray
  
    if show_image:
        cv2.imshow("c", resize(frame, 30)) 
        cv2.moveWindow("c", 0, 0)
        key = cv2.waitKey(1) 
        if key == ord('q'): 
            break

  
video.release() 
# Destroying all the windows 
cv2.destroyAllWindows() 

if len(motion_list) > 0:
    m = motion_list.pop()
    if len(m) < 2:
        motion_list.append((m[0], timecount))
    else:
        motion_list.append(m)
print(f"Read {framecount} frames.")
if len(motion_list) > 0:
    for l in motion_list:
        print(l)

    import moviepy.editor as mvpye
    clip = mvpye.VideoFileClip(clipname)
    subclips = [] 
    for l in motion_list:
        subclips.append(clip.subclip(l[0] / 1000, l[1] / 1000))
    result = mvpye.concatenate_videoclips(subclips)
    result.write_videofile(os.path.basename(clipname) + "-cut.mp4")
else:
    print("No bigger motion detected.")


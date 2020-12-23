import cv2
import sys

if __name__ == '__main__':
    fn = sys.argv[1]
    cap = cv2.VideoCapture(fn)


    if not cap.isOpened(): 
        print("could not open :", fn)
    

    l = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps    = cap.get(cv2.CAP_PROP_FPS)

    print(f"l {l}, w {w} w, h {h}, fps {fps}.")

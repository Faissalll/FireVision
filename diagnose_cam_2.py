
import cv2
import time

url = "http://192.168.110.161:4747/video"
print(f"Testing OpenCV on: {url}")

cap = cv2.VideoCapture(url)
if cap.isOpened():
    print("SUCCESS: Stream opened!")
    ret, frame = cap.read()
    if ret:
        print("SUCCESS: Frame read.")
    else:
        print("WARNING: Stream open but empty frame.")
else:
    print("FAIL: Could not open stream.")
cap.release()

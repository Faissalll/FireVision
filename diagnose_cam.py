
import cv2
import requests

base_url = "http://192.168.110.161:4747"
paths = ["/mjpegfeed", "/video", "/video/mjpeg", "/stream", "/live"]

print(f"--- DIAGNOSTIC START ---")
print(f"Target Base: {base_url}")

found_url = None

for path in paths:
    test_url = base_url + path
    print(f"\nTesting Path: {path}")
    try:
        response = requests.get(test_url, stream=True, timeout=2)
        print(f"HTTP Status: {response.status_code}")
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', '')
            print(f"Content-Type: {content_type}")
            if 'image' in content_type or 'multipart' in content_type:
                print(">>> POSSIBLE STREAM FOUND! <<<")
                found_url = test_url
                break
    except Exception as e:
        print(f"Error: {e}")

if found_url:
    print(f"\nVerifying with OpenCV: {found_url}")
    cap = cv2.VideoCapture(found_url)
    if cap.isOpened():
        print("PASS: OpenCV opened the stream successfully!")
    else:
        print("FAIL: OpenCV could not open the stream.")
else:
    print("\nFAIL: No valid video stream path found.")

print(f"--- DIAGNOSTIC END ---")

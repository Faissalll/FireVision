import cv2
import os
import time
import math
import uuid
from datetime import datetime
from ultralytics import YOLO
# import mysql.connector (Removed for Microservice)
from .notifier import TelegramNotifier, EmailNotifier, SMSNotifier
# from ..database import get_db_connection (Removed for Microservice)

# Global State
model = None
sessions = {}

def load_model():
    global model
    # Adjust path to match original location relative to this file? 
    # Original: backend/best (17).pt
    # New file: backend/app/services/detector.py
    # Model is at: ../../best (17).pt
    
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) # backend/
    model_path = os.path.join(base_dir, 'best (17).pt')
    
    if not os.path.exists(model_path):
        print(f"Error: Model file not found at {model_path}")
        return False
    
    try:
        model = YOLO(model_path)
        print(f"✅ Model loaded successfully from {model_path}")
        return True
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return False

def detect_fire(frame, session_data):
    global model
    
    if model is None:
        return frame, False, []
    
    sensitivity = session_data["settings"].get("sensitivity", 70)
    conf_threshold = sensitivity / 100.0
    
    results = model(frame, conf=conf_threshold, verbose=False)
    
    fire_detected = False
    detections = []
    
    frame_counter = session_data["frame_counter"]
    blink_speed = 2
    alpha = (math.sin(frame_counter * blink_speed * 0.1) + 1) / 2
    alpha = 0.5 + (alpha * 0.5)
    session_data["frame_counter"] += 1
    
    for result in results:
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            
            confidence = float(box.conf[0])
            class_id = int(box.cls[0])
            
            if hasattr(model, "names"):
                class_name = model.names[class_id]
            else:
                class_name = str(class_id)
            
            fire_detected = True
            box_color = (0, 0, 255)  
            
            cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)
            
            label = f"{class_name}: {confidence:.1%}"
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                        0.6, (255, 255, 255), 2, cv2.LINE_AA)
            
            detections.append({
                "class": class_name,
                "confidence": confidence,
                "bbox": [x1, y1, x2, y2],
            })
            
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cv2.putText(frame, timestamp, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                0.7, (255, 255, 255), 2, cv2.LINE_AA)
    
    status_text = (
        f'🔥 FIRE DETECTED! ({len(detections)})' if fire_detected 
        else '✓ System Active'
    )
    status_color = (0, 0, 255) if fire_detected else (0, 255, 0)
    
    cv2.rectangle(frame, (5, 45), (350, 75), status_color, -1)
    cv2.putText(frame, status_text, (10, 68), cv2.FONT_HERSHEY_SIMPLEX, 
                0.7, (255, 255, 255), 2, cv2.LINE_AA)
    
    return frame, fire_detected, detections

def generate_frames(session_id):
    global sessions
    # Note: notifier usage here needs to be adapted
    
    if session_id not in sessions:
        print(f"❌ Session {session_id} not found in generate_frames")
        return

    session = sessions[session_id]
    print(f"🎥 Starting stream for session: {session_id}")

    # Fallback/Global SMS Notifier (legacy support)
    sms_notifier = None
    try:
        if os.getenv("FONNTE_API_KEY") and os.getenv("SMS_PHONE_NUMBER"):
             sms_notifier = SMSNotifier(os.getenv("FONNTE_API_KEY"))
    except: pass

    while session["is_detecting"]:
        camera = session["camera"]
        if camera is None:
            break


class FireDetector:
    def __init__(self, model_path="best (2).pt"):
        self.model = YOLO(model_path)
        self.running = False
        self.cap = None
        
        # Configuration (Env Vars)
        self.rtsp_url = os.getenv('RTSP_URL', 'rtsp://admin:password@192.168.1.5:8080/h264')
        self.backend_url = os.getenv('BACKEND_URL', 'http://localhost:5000') # Railway URL
        self.webhook_secret = os.getenv('WEBHOOK_SECRET', 'rahasia123')
        self.username = os.getenv('OWNER_USERNAME', 'admin') # Who owns this stream
        
        # Debounce
        self.last_alert_time = 0
        self.alert_cooldown = 10 # Seconds

    def start_stream(self):
        self.running = True
        # Try opening RTSP
        print(f"🎥 Connecting to RTSP: {self.rtsp_url}")
        self.cap = cv2.VideoCapture(self.rtsp_url)
        
        if not self.cap.isOpened():
             print("❌ Failed to open RTSP stream. Using Dummy Video if available, else blank.")
             # Fallback logic here if needed
             
    def stop_stream(self):
        self.running = False
        if self.cap:
            self.cap.release()

    def generate_frames(self):
        while self.running:
            if not self.cap or not self.cap.isOpened():
                time.sleep(1)
                # Reconnect logic could go here
                self.cap = cv2.VideoCapture(self.rtsp_url)
                continue

            success, frame = self.cap.read()
            if not success:
                # If RTSP drops, wait and retry
                self.cap.release()
                time.sleep(1)
                continue

            # Detection
            results = self.model(frame, conf=0.4, verbose=False)
            annotated_frame = results[0].plot()

            # Check Fire
            detected = False
            confidence = 0
            for box in results[0].boxes:
                cls_id = int(box.cls[0])
                if self.model.names[cls_id].lower() in ['fire', 'smoke']:
                    detected = True
                    confidence = float(box.conf[0])
                    break
            
            # Send Webhook Alert
            if detected:
                self.send_alert(confidence, annotated_frame)

            # Encode for streaming
            params = [cv2.IMWRITE_JPEG_QUALITY, 80 if detected else 60]
            ret, buffer = cv2.imencode('.jpg', annotated_frame, params)
            frame_bytes = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    def send_alert(self, confidence, frame):
        now = time.time()
        if now - self.last_alert_time < self.alert_cooldown:
            return

        self.last_alert_time = now
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"🔥 FIRE DETECTED! Sending webhook to {self.backend_url}")
        
        try:
             # Convert frame to base64 for preview (optional)
             _, buf = cv2.imencode('.jpg', frame)
             img_b64 = base64.b64encode(buf).decode('utf-8')
             
             payload = {
                 "username": self.username,
                 "confidence": confidence,
                 "timestamp": timestamp,
                 # "image_base64": img_b64 # Heavy payload, enable if needed
             }
             
             headers = {
                 "X-Webhook-Secret": self.webhook_secret,
                 "Content-Type": "application/json"
             }
             
             url = f"{self.backend_url}/api/webhook/fire-alert"
             requests.post(url, json=payload, headers=headers, timeout=5)
             
        except Exception as e:
            print(f"❌ Failed to send webhook: {e}")
            
# Singleton
fire_service = FireDetector()

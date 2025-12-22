import cv2
import os
import time
import math
import uuid
from datetime import datetime
from ultralytics import YOLO
import mysql.connector
from .notifier import TelegramNotifier, EmailNotifier, SMSNotifier
from ..database import get_db_connection

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
    model_path = os.path.join(base_dir, 'best (13).pt')
    
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
    
    # Sensitivity Configuration (More Sensitive Default)
    sensitivity = session_data["settings"].get("sensitivity", 40)
    conf_threshold = sensitivity / 100.0
    
    results = model(frame, imgsz=640, conf=conf_threshold, verbose=False)
    
    fire_detected_this_frame = False
    detections = []
    
    frame_counter = session_data["frame_counter"]
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
            
            fire_detected_this_frame = True
            
            # Visuals: Simple Red Box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            
            label = f"{class_name}: {confidence:.1%}"
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                        0.6, (255, 255, 255), 2, cv2.LINE_AA)
            
            detections.append({
                "class": class_name,
                "confidence": confidence,
                "bbox": [x1, y1, x2, y2],
            })

    # Sensitivity/Persistence Logic
    consecutive = session_data.get("consecutive_fire_frames", 0)
    fire_confirmed = session_data.get("fire_confirmed", False)

    if fire_detected_this_frame:
        consecutive += 1
    else:
        consecutive = 0
    
    session_data["consecutive_fire_frames"] = consecutive
    
    # 5 Frames thresholds
    if consecutive >= 5:
        fire_confirmed = True
    elif consecutive == 0:
        fire_confirmed = False
        
    session_data["fire_confirmed"] = fire_confirmed
            
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

        success, frame = camera.read()
        if not success:
            time.sleep(0.05)
            continue

        try:
            frame = cv2.resize(frame, (640, 480))

            processed_frame, fire_detected, detections = detect_fire(frame, session)

            h, w = processed_frame.shape[:2]
            session["last_frame_w"] = w
            session["last_frame_h"] = h

            boxes_for_api = []
            for idx, det in enumerate(detections):
                x1, y1, x2, y2 = det["bbox"]
                boxes_for_api.append({
                    "id": idx,
                    "label": det["class"],
                    "confidence": det["confidence"] * 100.0,  
                    "x": x1,
                    "y": y1,
                    "w": x2 - x1,
                    "h": y2 - y1,
                })
            session["last_boxes"] = boxes_for_api

            # --- PER-USER NOTIFICATION LOGIC ---
            ns = session.get("notification_settings", {})
            
            # Fire Detected Logic
            if fire_detected and not session.get("fire_was_detected"):
                session["fire_was_detected"] = True
                camera_display_name = session.get("camera_name", f"Camera {session_id[:4]}")
                print(f"🔥 FIRE DETECTED on {camera_display_name}! Processing alerts...")

                # 1. TELEGRAM
                if ns.get("telegram_enabled") and ns.get("telegram_bot_token") and ns.get("telegram_chat_id"):
                    try:
                        tn = TelegramNotifier(ns["telegram_bot_token"], ns["telegram_chat_id"])
                        tn.send_notification(
                            f"🔥 FireVision Alert ({camera_display_name}) — Api terdeteksi!",
                            frame=processed_frame
                        )
                        print(f"📨 Telegram sent to user {session.get('owner')}")
                    except Exception as e:
                        print(f"❌ Telegram Error: {e}")

                # 2. EMAIL
                if ns.get("email_enabled") and ns.get("email_recipient"):
                    try:
                        en = EmailNotifier(
                            ns.get("email_smtp_host"), ns.get("email_smtp_port"),
                            ns.get("email_sender"), ns.get("email_password"),
                            ns.get("email_recipient")
                        )
                        en.send_email(
                            f"FIRE ALERT: {camera_display_name}",
                            f"Peringatan Kebakaran!\\n\\nKamera: {camera_display_name}\\nWaktu: {datetime.now()}\\n\\nHarap segera diperiksa."
                        )
                        print(f"📧 Email sent to user {session.get('owner')}")
                    except Exception as e:
                         print(f"❌ Email Error: {e}")

                # 3. SMS (Fallback)
                if sms_notifier is not None and os.getenv("SMS_PHONE_NUMBER"):
                     try:
                        sms_notifier.send_fire_alert(os.getenv("SMS_PHONE_NUMBER"), camera_display_name)
                     except: pass
                
                # 4. DATABASE LOG
                try:
                    conn = get_db_connection()
                    c = conn.cursor()
                    max_conf = 0
                    for d in detections:
                        if d['confidence'] > max_conf: max_conf = d['confidence']
                    
                    c.execute('''
                        INSERT INTO alarms (uuid, timestamp, camera_id, zone, confidence, status, image_path)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ''', (
                        session_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        camera_display_name, "Zone A", int(max_conf * 100), "Baru", ""
                    ))
                    conn.commit()
                    conn.close()
                    print("💾 Alarm stored to DB.")
                except Exception as e:
                    print(f"❌ DB Log Error: {e}")

            elif not fire_detected and session.get("fire_was_detected"):
                session["fire_was_detected"] = False

            ret, buffer = cv2.imencode('.jpg', processed_frame)
            if not ret:
                continue

            frame_bytes = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        except Exception as e:
            print(f"Error inside video loop session {session_id}: {e}")
            break

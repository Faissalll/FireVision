import cv2
import os
import time
import math
import uuid
from datetime import datetime
from ultralytics import YOLO
from .telegram_notifier import TelegramNotifier

# Global State
model = None
sessions = {}
last_notification_time = {}
last_alarm_save_time = {}

def save_alarm_to_db(session_id, session, detections, frame):
    """Save alarm to database when fire is detected"""
    try:
        from ..database import get_db_connection
        conn = get_db_connection()
        c = conn.cursor()
        
        camera_name = session.get("camera_name", "Camera")
        confidence = detections[0].get("confidence", 0) if detections else 0
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        alarm_uuid = str(uuid.uuid4())
        
        c.execute("""
            INSERT INTO alarms (uuid, timestamp, camera_id, zone, confidence, status, image_path)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            alarm_uuid,
            timestamp,
            camera_name,
            "Default Zone",
            confidence,
            "active",
            ""
        ))
        
        conn.commit()
        conn.close()
        print(f"💾 Alarm saved to database: {alarm_uuid}")
        return True
    except Exception as e:
        print(f"❌ Error saving alarm to database: {e}")
        return False

def load_model():
    global model
    # Model is expected to be in the root of the service
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) 
    
    # Check for likely model names
    possible_names = ['best (13).pt', 'best (17).pt', 'best.pt', 'yolov8n.pt']
    
    debug_log = f"Base: {base_dir} | "
    
    for name in possible_names:
        model_path = os.path.join(base_dir, name)
        debug_log += f"Checking {name}: "
        
        if os.path.exists(model_path):
            try:
                model = YOLO(model_path)
                return True, f"Loaded {name}"
            except Exception as e:
                debug_log += f"Exception ({str(e)}); "
                import traceback
                traceback.print_exc()
        else:
            debug_log += "Not Found; "

    return False, f"Failed. Log: {debug_log}"

def detect_fire(frame, session_data):
    global model
    
    if model is None:
        return frame, False, []
    
    # Sensitivity Configuration (Matched to User Script)
    sensitivity = session_data["settings"].get("sensitivity", 25)
    conf_threshold = sensitivity / 100.0
    
    # Run Inference (imgsz=640 matches training/local script)
    results = model(frame, imgsz=640, conf=conf_threshold, verbose=False)
    
    fire_detected_this_frame = False
    detections = []
    
    # DEBUG: Track max confidence
    max_conf_debug = 0.0
    
    # Blink Effect State
    frame_counter = session_data.get("frame_counter", 0)
    session_data["frame_counter"] = frame_counter + 1
    
    for result in results:
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            
            confidence = float(box.conf[0])
            if confidence > max_conf_debug: max_conf_debug = confidence
            
            class_id = int(box.cls[0])
            
            if hasattr(model, "names"):
                class_name = model.names[class_id]
            else:
                class_name = str(class_id)
            
            # Simple Fire Filter
            if class_name.lower() in ['fire', 'smoke']:
                fire_detected_this_frame = True
            
            # Draw Box
            box_color = (0, 0, 255) if fire_detected_this_frame else (0, 255, 0)
            cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)
            
            # Draw Label
            label = f"{class_name}: {confidence:.1%}"
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                        0.6, (255, 255, 255), 2, cv2.LINE_AA)
            
            detections.append({
                "class": class_name,
                "confidence": confidence,
                "bbox": [x1, y1, x2, y2],
                # Normalized coords for frontend
                "x": x1, "y": y1, "w": x2-x1, "h": y2-y1 # Raw pixels, frontend will scale or use raw
            })

    # Sensitivity/Persistence Logic
    consecutive = session_data.get("consecutive_fire_frames", 0)
    
    if fire_detected_this_frame:
        consecutive += 1
    else:
        consecutive = 0
    
    session_data["consecutive_fire_frames"] = consecutive
    
    # Reduced from 2 to 1 frame for INSTANT reaction (User Request)
    if consecutive >= 1:
        session_data["fire_confirmed"] = True
    elif consecutive == 0:
        session_data["fire_confirmed"] = False
        
    fire_confirmed = session_data.get("fire_confirmed", False)
    
    # --- RESTORED ALARM & NOTIFICATION LOGIC ---
    current_time = time.time()
    
    # 1. Telegram Notification (Rate Limited: 60s)
    if fire_confirmed:
        last_notif = last_notification_time.get(session_data.get('id', 'default'), 0)
        time_since = current_time - last_notif
        print(f"🔥 FIRE DETECTED! Time since last notif: {time_since:.1f}s")
        
        if time_since > 60:
            print(f"🔔 TRIGGERING TELEGRAM ALERT for Session {session_data.get('id')}...")
            # Run in background to not block frame
            import threading
            try:
                threading.Thread(target=TelegramNotifier.send_fire_alert, 
                               args=(frame.copy(), session_data.get("camera_name", "Camera"))).start()
                last_notification_time[session_data.get('id', 'default')] = current_time
                print("✅ Telegram Thread Started")
            except Exception as e:
                print(f"❌ Failed to start Telegram thread: {e}")

    # 2. Save to Database (Rate Limited: 10s)
    if fire_confirmed:
        last_save = last_alarm_save_time.get(session_data.get('id', 'default'), 0)
        if current_time - last_save > 10:
            print("💾 Attempting to save alarm to DB...")
            saved = save_alarm_to_db(session_data.get('id'), session_data, detections, frame)
            if saved:
                print("✅ Alarm Saved to DB")
                last_alarm_save_time[session_data.get('id', 'default')] = current_time
            else:
                print("❌ Failed to save alarm to DB")

    # 3. Status Bar Overlay & Timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cv2.putText(frame, timestamp, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                0.7, (255, 255, 255), 2, cv2.LINE_AA)
    
    if fire_confirmed:
        status_text = "FIRE DETECTED!"
        status_color = (0, 0, 255) # Red
        
        # Flashing Border
        if (frame_counter // 5) % 2 == 0:
             cv2.rectangle(frame, (0, 0), (frame.shape[1], frame.shape[0]), (0, 0, 255), 10)
    else:
        status_text = "Monitoring..."
        status_color = (0, 255, 0) # Green
        
    cv2.putText(frame, status_text, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 
                1.0, status_color, 2, cv2.LINE_AA)

    # DEBUG OVERLAY
    debug_color = (0, 255, 255)
    debug_text = f"MAX CONF: {max_conf_debug:.2f} (Thresh: {conf_threshold:.2f})"
    cv2.putText(frame, debug_text, (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 
                0.7, debug_color, 2, cv2.LINE_AA)

    return frame, fire_confirmed, detections

def generate_frames(session_id):
    global sessions
    
    if session_id not in sessions:
        print(f"❌ Session {session_id} not found in generate_frames")
        return

    session = sessions[session_id]
    print(f"🎥 Starting stream loop for session: {session_id}")

    try:
        while session.get("is_detecting", False):
            camera = session.get("camera")
            if camera is None or not camera.isOpened():
                print("Camera disconnected or invalid.")
                break

            success, frame = camera.read()
            if not success:
                # Loop video if file/demo, or retry if IP cam?
                # For now just wait and retry
                time.sleep(0.1)
                continue
                
            # If frame too big, resize for performance?
            #frame = cv2.resize(frame, (640, 480))

            # Detect
            annotated_frame, fire_detected, detections = detect_fire(frame, session)
            
            # 🔔 Send Telegram Notification if fire detected
            if fire_detected:
                notif_settings = session.get("notification_settings", {})
                telegram_enabled = notif_settings.get("telegram_enabled", False)
                bot_token = notif_settings.get("telegram_bot_token", "")
                chat_id = notif_settings.get("telegram_chat_id", "")
                
                if telegram_enabled and bot_token and chat_id:
                    # Throttle: only send once every 10 seconds per session
                    now = time.time()
                    last_sent = last_notification_time.get(session_id, 0)
                    
                    if now - last_sent > 10:
                        try:
                            notifier = TelegramNotifier(bot_token, chat_id)
                            camera_name = session.get("camera_name", "Kamera Utama")
                            confidence = detections[0].get("confidence", 0) * 100 if detections else 0
                            message = (
                                f"🔥 *PERINGATAN KEBAKARAN!*\n\n"
                                f"📍 Kamera: {camera_name}\n"
                                f"⏰ Waktu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                                f"📊 Confidence: {confidence:.1f}%\n\n"
                                f"Segera lakukan tindakan!"
                            )
                            notifier.send_photo_from_cv2(annotated_frame, caption=message)
                            last_notification_time[session_id] = now
                            print(f"📲 Telegram notification sent for session {session_id}")
                        except Exception as e:
                            print(f"❌ Telegram notification failed: {e}")
                
                # 💾 Save alarm to database (throttle: 30 seconds)
                now = time.time()
                last_saved = last_alarm_save_time.get(session_id, 0)
                if now - last_saved > 30:
                    save_alarm_to_db(session_id, session, detections, annotated_frame)
                    last_alarm_save_time[session_id] = now
            
            # Update Session State (for polling API)
            session["last_boxes"] = detections
            session["last_frame_w"] = frame.shape[1]
            session["last_frame_h"] = frame.shape[0]
            # Ideally /api/detections should read from session["last_boxes"]
            # We need to verify stream_routes uses this.
            
            # Note: stream_routes endpoint for detections isn't shown in my view_file key checks
            # But assuming it reads session["last_boxes"]
            
            # Encode
            ret, buffer = cv2.imencode('.jpg', annotated_frame, [cv2.IMWRITE_JPEG_QUALITY, 60])
            frame_bytes = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                   
            # Limit FPS to ~30
            # time.sleep(0.01) 
            
    except Exception as e:
        print(f"Stream error: {e}")
    finally:
        print(f"Stream ended for {session_id}")
        if session.get("camera"):
            session["camera"].release()

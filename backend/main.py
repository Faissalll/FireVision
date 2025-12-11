from flask import Flask, Response, request, jsonify
from flask_cors import CORS
from datetime import datetime
from ultralytics import YOLO
import cv2
import os
import time
import uuid
import math
import numpy as np  

from telegram_notifier import TelegramNotifier
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

sessions = {}

model = None

try:
    notifier = TelegramNotifier(
        token=os.getenv("TELEGRAM_BOT_TOKEN"),
        chat_id=os.getenv("TELEGRAM_CHAT_ID"),
    )
    print("✅ Telegram Notifier konfigurasi dari .env")
except Exception as e:
    notifier = None
    print(f"⚠️ Telegram Notifier tidak aktif: {e}")


def load_model():
    global model
    model_path = os.path.join(os.path.dirname(__file__), 'best (17).pt')
    
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
    global sessions, notifier

    if session_id not in sessions:
        print(f"❌ Session {session_id} not found in generate_frames")
        return

    session = sessions[session_id]
    print(f"🎥 Starting stream for session: {session_id}")

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

            if notifier is not None:
                if fire_detected and not session["fire_was_detected"]:
                    session["fire_was_detected"] = True
                    try:
                        notifier.send_notification(
                            f"🔥 FireVision Alert (Cam {session_id[:4]}) — Api terdeteksi!",
                            frame=processed_frame
                        )
                        print("📨 Telegram alert sent.")
                        
                        try:
                            conn = mysql.connector.connect(
                                host=os.getenv('DB_HOST', 'localhost'),
                                user=os.getenv('DB_USER', 'root'),
                                password=os.getenv('DB_PASSWORD', ''),
                                database=os.getenv('DB_NAME', 'firevision')
                            )
                            c = conn.cursor()
                            
                            max_conf = 0
                            for d in detections:
                                if d['confidence'] > max_conf:
                                    max_conf = d['confidence']
                            
                            c.execute('''
                                INSERT INTO alarms (uuid, timestamp, camera_id, zone, confidence, status, image_path)
                                VALUES (%s, %s, %s, %s, %s, %s, %s)
                            ''', (
                                session_id,
                                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                f"Camera {session_id[:4]}", 
                                "Zone A", 
                                int(max_conf * 100),
                                "Baru",
                                ""
                            ))
                            conn.commit()
                            conn.close()
                            print("💾 Alarm stored to DB.")
                        except Exception as e:
                            print(f"❌ Database error: {e}")
                            
                    except Exception as e:
                        print(f"❌ Gagal kirim Telegram: {e}")

                elif not fire_detected and session["fire_was_detected"]:
                    session["fire_was_detected"] = False
                    try:
                        notifier.send_notification(
                            f"✅ Api telah padam (Cam {session_id[:4]}) — kondisi aman."
                        )
                        print("📨 Telegram cleared sent.")
                        
                    except Exception as e:
                        print(f"❌ Gagal kirim Telegram: {e}")

            ret, buffer = cv2.imencode('.jpg', processed_frame)
            if not ret:
                continue

            frame_bytes = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        except Exception as e:
            print(f"Error inside video loop session {session_id}: {e}")
            break


@app.route('/')
def index():
    return jsonify({'status': 'running', 'message': 'FireVision API is Online (Multi-Camera Support)'})


@app.route('/api/start-detection', methods=['POST'])
def start_detection():
    global model, sessions
    
    try:
        if model is None:
            print("Loading YOLO model...")
            if not load_model():
                return jsonify({'error': 'Failed to load model best.pt'}), 500
        
        data = request.get_json() or {}

        username = data.get('username')
        if not username:
             return jsonify({'error': 'Username required'}), 400

        # Enforce Camera Limits
        active_count = 0
        for s_id, s_data in sessions.items():
            if s_data.get('owner') == username and s_data.get('is_detecting'):
                active_count += 1
        
        # Check Plan
        user_plan = 'free' # Default
        try:
            conn = get_db_connection()
            c = conn.cursor(dictionary=True)
            c.execute("SELECT plan FROM users WHERE username = %s", (username,))
            row = c.fetchone()
            if row:
                user_plan = row['plan']
            conn.close()
        except Exception as e:
            print(f"Error checking plan: {e}")

        MAX_FREE_CAMERAS = 2
        
        if user_plan == 'free' and active_count >= MAX_FREE_CAMERAS:
            return jsonify({
                'error': f'Limit Tercapai! Pengguna Free hanya bisa menggunakan {MAX_FREE_CAMERAS} kamera. Upgrade ke Premium untuk akses unlimited.'
            }), 403

        camera_source = str(data.get('camera_source', 'WEBCAM')).upper()
        ip_camera_url = data.get('ip_camera_url') 

        initial_settings = {
            "sensitivity": data.get("sensitivity", 70),
            "camera_source": camera_source,
            "ip_camera_url": ip_camera_url,
            "smoothing": data.get("smoothing", False),
            "noiseReduction": data.get("noiseReduction", False),
            "playbackControls": data.get("playbackControls", False),
        }
        
        session_id_str = str(uuid.uuid4())
        
        print(f"📷 Request Start Camera. Source: {camera_source}")

        camera_obj = None

        if camera_source == 'IPHONE' or camera_source == 'IP_CAMERA':
            if not ip_camera_url:
                return jsonify({'error': 'URL IP Camera kosong!'}), 400
            
            print(f"Connecting to IP Camera at: {ip_camera_url}")
            camera_obj = cv2.VideoCapture(ip_camera_url)
            camera_obj.set(cv2.CAP_PROP_BUFFERSIZE, 1)

            if not camera_obj.isOpened():
                print("Kamera IP gagal dibuka, coba lagi...")
                time.sleep(1)
                camera_obj = cv2.VideoCapture(ip_camera_url)
        
        else:
            cam_idx = data.get('camera_index', 0)
            print(f"Connecting to Webcam (Index {cam_idx})...")
            camera_obj = cv2.VideoCapture(cam_idx, cv2.CAP_DSHOW)
            if not camera_obj.isOpened():
                print(f"Index {cam_idx} gagal, mencoba fallback ke 0...")
                camera_obj = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        if not camera_obj or not camera_obj.isOpened():
            print("❌ GAGAL: Kamera tidak bisa dibuka.")
            return jsonify({'error': 'Failed to open camera. Check connection/URL.'}), 500

        sessions[session_id_str] = {
            "camera": camera_obj,
            "is_detecting": True,
            "settings": initial_settings,
            "last_boxes": [],
            "last_frame_w": 0,
            "last_frame_h": 0,
            "fire_was_detected": False,
            "fire_was_detected": False,
            "frame_counter": 0,
            "owner": username
        }

        print(f"✅ Camera Session Started! ID: {session_id_str}")
        
        return jsonify({
            'status': 'started',
            'session_id': session_id_str
        })
        
    except Exception as e:
        print(f"Error starting detection: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/update-settings', methods=['POST'])
def update_settings():
    global sessions
    data = request.get_json() or {}
    
    target_session_id = data.get('session_id')
    
    if target_session_id:
        if target_session_id in sessions:
            settings = sessions[target_session_id]["settings"]
            if 'sensitivity' in data: settings['sensitivity'] = data['sensitivity']
            if 'smoothing' in data: settings['smoothing'] = data['smoothing']
            if 'noiseReduction' in data: settings['noiseReduction'] = data['noiseReduction']
            return jsonify({'status': 'updated', 'session_id': target_session_id})
        else:
            return jsonify({'error': 'Session not found'}), 404
    else:
        for sid in sessions:
            settings = sessions[sid]["settings"]
            if 'sensitivity' in data: settings['sensitivity'] = data['sensitivity']
            if 'smoothing' in data: settings['smoothing'] = data['smoothing']
            if 'noiseReduction' in data: settings['noiseReduction'] = data['noiseReduction']
        return jsonify({'status': 'updated_all'})


@app.route('/api/stop-detection', methods=['POST'])
def stop_detection():
    global sessions
    data = request.get_json() or {}
    target_session_id = data.get('session_id')

    if target_session_id:
        if target_session_id in sessions:
            session = sessions[target_session_id]
            session["is_detecting"] = False
            time.sleep(0.5) 
            if session["camera"]:
                session["camera"].release()
            del sessions[target_session_id]
            print(f"🛑 Session stopped: {target_session_id}")
            return jsonify({'status': 'stopped', 'session_id': target_session_id})
        else:
            return jsonify({'status': 'not_found_or_already_stopped'})
    else:
        if data.get('stop_all') is True:
            print("🛑 Stopping ALL sessions...")
            ids = list(sessions.keys())
            for sid in ids:
                sessions[sid]["is_detecting"] = False
                if sessions[sid]["camera"]:
                    sessions[sid]["camera"].release()
            sessions.clear()
            return jsonify({'status': 'stopped_all'})
        else:
            print("⚠️ Warning: stop-detection called without session_id. Ignoring to prevent stopping all sessions.")
            return jsonify({'status': 'ignored_missing_session_id'}), 200

@app.route('/api/video-feed')
def video_feed():
    session_id = request.args.get('session')
    if not session_id:
        return "Missing session parameter", 400
    
    return Response(
        generate_frames(session_id), 
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


from werkzeug.security import generate_password_hash, check_password_hash

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'firevision')
    )

def init_db():
    conn = None
    try:
        # Connect to MySQL Server first to create DB if not exists
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', '')
        )
        c = conn.cursor()
        db_name = os.getenv('DB_NAME', 'firevision')
        c.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        conn.close()

        # Connect to the specific database
        conn = get_db_connection()
        c = conn.cursor()
        
        # Table Alarms
        c.execute('''
            CREATE TABLE IF NOT EXISTS alarms (
                id INT AUTO_INCREMENT PRIMARY KEY,
                uuid VARCHAR(255),
                timestamp VARCHAR(255),
                camera_id VARCHAR(255),
                zone VARCHAR(255),
                confidence REAL,
                status VARCHAR(50), 
                image_path TEXT
            )
        ''')
        
        # Table Users
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) UNIQUE,
                password VARCHAR(255),
                plan VARCHAR(50) DEFAULT 'free'
            )
        ''')

        # Migration: Add plan column if not exists (for existing tables)
        try:
            c.execute("SELECT plan FROM users LIMIT 1")
            c.fetchall() 
        except Exception:
            print("⚠️ 'plan' column missing in users. Adding it...")
            try:
                c.execute("ALTER TABLE users ADD COLUMN plan VARCHAR(50) DEFAULT 'free'")
            except Exception as e_alter:
                print(f"❌ Failed to alter table: {e_alter}")
        
        conn.commit()
        conn.close()
        print(f"✅ Database initialized ({db_name}: alarms, users)")
    except Exception as e:
        print(f"❌ Error initializing DB: {e}")

init_db()

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username dan password wajib diisi'}), 400

    hashed_password = generate_password_hash(password)

    try:
        conn = get_db_connection()
        c = conn.cursor()
        # Default plan is 'free'
        c.execute("INSERT INTO users (username, password, plan) VALUES (%s, %s, 'free')", (username, hashed_password))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success', 'message': 'Registrasi berhasil!'})
    except mysql.connector.Error as err:
        if err.errno == 1062: # Duplicate entry
            return jsonify({'error': 'Username sudah digunakan'}), 409
        return jsonify({'error': str(err)}), 500
    except Exception as e:
        print(f"Error register: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username dan password wajib diisi'}), 400

    try:
        conn = get_db_connection()
        c = conn.cursor(dictionary=True)
        c.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            return jsonify({
                'status': 'success', 
                'message': 'Login berhasil', 
                'username': username,
                'plan': user.get('plan', 'free') 
            })
        else:
            return jsonify({'error': 'Username atau password salah'}), 401
            
    except Exception as e:
        print(f"Error login: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'running',
        'active_sessions': len(sessions)
    })


@app.route('/api/history', methods=['GET'])
def get_history():
    try:
        conn = get_db_connection()
        c = conn.cursor(dictionary=True)
        
        c.execute("SELECT * FROM alarms ORDER BY id DESC")
        rows = c.fetchall()
        
        history = []
        for row in rows:
            history.append({
                "id": f"ALM-{row['id']:03d}", 
                "db_id": row['id'],
                "uuid": row['uuid'],
                "time": row['timestamp'].split(' ')[1] if row['timestamp'] else "",
                "date": row['timestamp'].split(' ')[0] if row['timestamp'] else "",
                "camera": row['camera_id'],
                "zone": row['zone'],
                "confidence": row['confidence'],
                "status": row['status'],
                "image_path": row['image_path']
            })
        
        conn.close()
        return jsonify(history)
    except Exception as e:
        print(f"Error fetching history: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/history/update-status', methods=['POST'])
def update_history_status():
    data = request.get_json() or {}
    db_id = data.get('db_id')
    new_status = data.get('status')
    
    if not db_id or not new_status:
        return jsonify({'error': 'Missing db_id or status'}), 400
        
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("UPDATE alarms SET status = %s WHERE id = %s", (new_status, db_id))
        conn.commit()
        conn.close()
        return jsonify({'status': 'updated', 'db_id': db_id, 'new_status': new_status})
    except Exception as e:
        print(f"Error updating history: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/detections', methods=['GET'])
def get_detections():
    global sessions
    session_id = request.args.get('session')
    
    if session_id and session_id in sessions:
        session = sessions[session_id]
        return jsonify({
            "boxes": session["last_boxes"],
            "frame_w": session["last_frame_w"],
            "frame_h": session["last_frame_h"],
        })
    return jsonify({"boxes": [], "error": "Session not found"})


@app.route('/api/detect', methods=['POST'])
def detect_single_frame():
    global model, notifier

    print("=== /api/detect dipanggil ===")
    
    if model is None:
        if not load_model():
            return jsonify({'error': 'Model not loaded'}), 500

    file = request.files.get('file')
    if file is None or file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        raw = file.read()
        file_bytes = np.frombuffer(raw, np.uint8)
        frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        if frame is None:
            return jsonify({'error': 'Failed to decode image'}), 400

        try:
            sensitivity = int(request.form.get('sensitivity', 70))
        except:
            sensitivity = 70

        dummy_session = {
            "settings": {"sensitivity": sensitivity},
            "frame_counter": 0
        }
        
        processed_frame, fire_detected, detections = detect_fire(frame, dummy_session)

        if fire_detected and notifier is not None:
             pass

        return jsonify({
            'fire_detected': fire_detected,
            'detections': detections,
            'sensitivity': sensitivity
        })

    except Exception as e:
        print(f"Error in /api/detect: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("=" * 60)
    print("🔥 FIREVISION SERVER (Refactored for Multi-Session)")
    print("=" * 60)
    
    load_model()
    
    print("\nMenunggu koneksi...")
    app.run(host='0.0.0.0', port=5001, debug=False, threaded=True)

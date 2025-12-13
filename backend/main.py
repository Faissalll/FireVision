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
from sms_notifier import SMSNotifier
from email_notifier import EmailNotifier
import jwt
import datetime
from functools import wraps
import mysql.connector
from dotenv import load_dotenv
import os

env_path = os.path.join(os.path.dirname(__file__), '.env')

def load_env_manual(path):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

load_env_manual(env_path)
print(f"🔑 TELEGRAM_BOT_TOKEN loaded: {os.getenv('TELEGRAM_BOT_TOKEN', 'NOT FOUND')[:20]}...")
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'FireVisionSecretKey2025!Secure')  # Change in production!

CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            # Bearer <token>
            if "Bearer" in token:
                token = token.split(" ")[1]
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['username']
        except Exception as e:
            return jsonify({'message': 'Token is invalid!', 'error': str(e)}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

sessions = {}

model = None

telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")

if telegram_token and telegram_chat_id and telegram_token != "YOUR_TELEGRAM_BOT_TOKEN":
    try:
        notifier = TelegramNotifier(
            token=telegram_token,
            chat_id=telegram_chat_id,
        )
        print("✅ Telegram Notifier konfigurasi dari .env")
    except Exception as e:
        notifier = None
        print(f"⚠️ Telegram Notifier tidak aktif: {e}")
else:
    notifier = None
    print(f"⚠️ Telegram Notifier tidak aktif: Token atau Chat ID kosong/invalid")

try:
    sms_notifier = SMSNotifier(
        api_key=os.getenv("FONNTE_API_KEY", "")
    )
    sms_phone = os.getenv("SMS_PHONE_NUMBER", "")
    if sms_phone and os.getenv("FONNTE_API_KEY"):
        print("✅ SMS Notifier konfigurasi dari .env")
    else:
        sms_notifier = None
        print("⚠️ SMS Notifier tidak aktif: API Key atau nomor HP kosong")
except Exception as e:
    sms_notifier = None
    print(f"⚠️ SMS Notifier tidak aktif: {e}")


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
                            f"Peringatan Kebakaran!\n\nKamera: {camera_display_name}\nWaktu: {datetime.now()}\n\nHarap segera diperiksa."
                        )
                        print(f"📧 Email sent to user {session.get('owner')}")
                    except Exception as e:
                         print(f"❌ Email Error: {e}")

                # 3. SMS (Keep existing global fallbacks if desired, or remove. Keeping for safety)
                if sms_notifier is not None and os.getenv("SMS_PHONE_NUMBER"):
                     try:
                        sms_notifier.send_fire_alert(os.getenv("SMS_PHONE_NUMBER"), camera_display_name)
                     except: pass
                
                # 4. DATABASE LOG
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


@app.route('/')
def index():
    return jsonify({'status': 'running', 'message': 'FireVision API is Online (Multi-Camera Support)'})


@app.route('/api/start-detection', methods=['POST'])
@token_required
def start_detection(current_user):
    global model, sessions
    
    try:
        if model is None:
            print("Loading YOLO model...")
            if not load_model():
                return jsonify({'error': 'Failed to load model best.pt'}), 500
        
        data = request.get_json() or {}

        username = current_user # Secure
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

        # Fetch Notification Settings
        notif_settings = {}
        try:
            conn = get_db_connection()
            c = conn.cursor(dictionary=True)
            c.execute("SELECT * FROM notification_settings WHERE username = %s", (username,))
            row = c.fetchone()
            conn.close()
            if row:
                notif_settings = row
                print(f"✅ Notification settings loaded for {username}")
        except Exception as e:
            print(f"❌ Error fetching notification settings: {e}")

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
        
        # Ambil nama kamera dari request (default: generic)
        camera_name_custom = data.get('camera_name', f'Camera {str(uuid.uuid4())[:4]}')
        
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
            "notification_settings": notif_settings,
            "fire_was_detected": False,
            "frame_counter": 0,
            "owner": username,
            "camera_name": camera_name_custom  # Simpan nama kamera
        }

        print(f"✅ Camera Session Started! ID: {session_id_str}")
        
        return jsonify({
            'status': 'started',
            'session_id': session_id_str
        })
        
    except Exception as e:
        print(f"Error starting detection: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/notification-settings', methods=['GET', 'POST'])
@token_required
def notification_settings_api(current_user):
    data = request.get_json(silent=True) or {}
    username = current_user # Use authenticated user, ignore request body username for security

    if not username:
        return jsonify({'error': 'Username required'}), 400

    conn = get_db_connection()
    c = conn.cursor(dictionary=True)

    if request.method == 'GET':
        try:
            c.execute("SELECT * FROM notification_settings WHERE username = %s", (username,))
            settings = c.fetchone()
            if not settings:
                # Return defaults
                settings = {
                    "username": username,
                    "telegram_enabled": False, "email_enabled": False,
                    "telegram_bot_token": "", "telegram_chat_id": "",
                    "email_smtp_host": "smtp.gmail.com", "email_smtp_port": 587,
                    "email_sender": "", "email_recipient": ""
                }
            return jsonify(settings)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            conn.close()

    elif request.method == 'POST':
        try:
            # UPSERT
            sql = """
            INSERT INTO notification_settings (
                username, telegram_enabled, telegram_bot_token, telegram_chat_id,
                email_enabled, email_smtp_host, email_smtp_port, email_sender, email_password, email_recipient
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                telegram_enabled=VALUES(telegram_enabled),
                telegram_bot_token=VALUES(telegram_bot_token),
                telegram_chat_id=VALUES(telegram_chat_id),
                email_enabled=VALUES(email_enabled),
                email_smtp_host=VALUES(email_smtp_host),
                email_smtp_port=VALUES(email_smtp_port),
                email_sender=VALUES(email_sender),
                email_password=VALUES(email_password),
                email_recipient=VALUES(email_recipient)
            """
            vals = (
                username,
                data.get('telegram_enabled', False),
                data.get('telegram_bot_token', ''),
                data.get('telegram_chat_id', ''),
                data.get('email_enabled', False),
                data.get('email_smtp_host', 'smtp.gmail.com'),
                data.get('email_smtp_port', 587),
                data.get('email_sender', ''),
                data.get('email_password', ''), # Be careful with plaintext passwords
                data.get('email_recipient', '')
            )
            c.execute(sql, vals)
            conn.commit()
            
            # TODO: Update active sessions for this user?
            # For simplicity, we just save. Next connection picks it up. 
            # Or iterate sessions:
            global sessions
            for sid, s in sessions.items():
                if s.get('owner') == username:
                    c.execute("SELECT * FROM notification_settings WHERE username = %s", (username,))
                    s['notification_settings'] = c.fetchone()
                    print(f"🔄 Updated live settings for session {sid}")

            return jsonify({'status': 'saved'})
        except Exception as e:
            print(f"Error saving settings: {e}")
            return jsonify({'error': str(e)}), 500
        finally:
            conn.close()


@app.route('/api/update-settings', methods=['POST'])
@token_required
def update_settings(current_user):
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
@token_required
def stop_detection(current_user):
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

        # Table Transactions
        c.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                order_id VARCHAR(255) UNIQUE,
                username VARCHAR(255),
                amount INT,
                status VARCHAR(50),
                snap_token VARCHAR(255),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Migration: Add plan column if not exists (for existing tables)
        try:
            # Table Notification Settings (NEW)
            c.execute("""
                CREATE TABLE IF NOT EXISTS notification_settings (
                    username VARCHAR(255) PRIMARY KEY,
                    telegram_enabled BOOLEAN DEFAULT FALSE,
                    telegram_bot_token TEXT,
                    telegram_chat_id TEXT,
                    email_enabled BOOLEAN DEFAULT FALSE,
                    email_smtp_host VARCHAR(255),
                    email_smtp_port INT DEFAULT 587,
                    email_sender VARCHAR(255),
                    email_password TEXT,
                    email_recipient TEXT,
                    FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
                )
            """)
        except Exception as e_notif:
            print(f"⚠️ Error creating notification_settings table: {e_notif}")

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
            # Generate Token
            token = jwt.encode({
                'username': username,
                'plan': user.get('plan', 'free'),
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }, app.config['SECRET_KEY'], algorithm="HS256")

            return jsonify({
                'status': 'success', 
                'message': 'Login berhasil', 
                'username': username,
                'plan': user.get('plan', 'free'),
                'token': token
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


# ==========================================
# PAYMENT GATEWAY (MIDTRANS) - Manual HTTP Request
# ==========================================
import requests
import base64
import json

# Konfigurasi Midtrans
midtrans_server_key = os.getenv('MIDTRANS_SERVER_KEY', 'SB-Mid-server-tOqB0d8a4X...') 
is_production = False  # Sandbox mode untuk testing

# Base URL Midtrans
midtrans_url = "https://app.midtrans.com/snap/v1/transactions" if is_production else "https://app.sandbox.midtrans.com/snap/v1/transactions"

@app.route('/api/payment/token', methods=['POST'])
def get_payment_token():
    try:
        data = request.get_json()
        username = data.get('username')
        plan_type = data.get('plan_type') # 'professional'
        price = data.get('price') # 799000

        if not username or not plan_type:
            return jsonify({'error': 'Data tidak lengkap'}), 400

        # Buat Order ID Unik
        order_id = f"ORDER-{int(time.time())}-{username}"
        
        # Payload untuk Midtrans Snap API
        payload = {
            "transaction_details": {
                "order_id": order_id,
                "gross_amount": price
            },
            "credit_card":{
                "secure": True
            },
            "customer_details": {
                "first_name": username,
                "email": f"{username.lower().replace(' ', '')}@gmail.com", 
            },
            "item_details": [{
                "id": plan_type,
                "price": price,
                "quantity": 1,
                "name": f"FireVision {plan_type.capitalize()} Plan"
            }]
        }

        # Auth Header (Basic Auth: ServerKey encoded in Base64 + :)
        auth_string = midtrans_server_key + ":"
        auth_header = base64.b64encode(auth_string.encode()).decode()
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Basic {auth_header}"
        }

        # Request ke Midtrans API
        response = requests.post(midtrans_url, json=payload, headers=headers)
        response_data = response.json()

        if response.status_code != 201:
            print(f"❌ Midtrans Error: {response_data}")
            return jsonify({'error': 'Gagal membuat transaksi midtrans'}), 500

        snap_token = response_data['token']
        # redirect_url = response_data['redirect_url']

        # Simpan Transaksi ke Database
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('''
            INSERT INTO transactions (order_id, username, amount, status, snap_token)
            VALUES (%s, %s, %s, 'pending', %s)
        ''', (order_id, username, price, snap_token))
        conn.commit()
        conn.close()

        return jsonify({
            'status': 'success',
            'token': snap_token,
            'order_id': order_id
        })

    except Exception as e:
        print(f"❌ Error Payment Token: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/payment/notification', methods=['POST'])
def payment_notification():
    try:
        notification_body = request.get_json()
        
        order_id = notification_body.get('order_id')
        transaction_status = notification_body.get('transaction_status')
        fraud_status = notification_body.get('fraud_status')

        print(f"🔔 Payment Notification: {order_id} - {transaction_status}")

        final_status = 'pending'
        if transaction_status == 'capture':
            if fraud_status == 'challenge':
                final_status = 'challenge'
            else:
                final_status = 'success'
        elif transaction_status == 'settlement':
            final_status = 'success'
        elif transaction_status == 'cancel' or transaction_status == 'deny' or transaction_status == 'expire':
            final_status = 'failed'
        elif transaction_status == 'pending':
            final_status = 'pending'

        conn = get_db_connection()
        c = conn.cursor()
        
        c.execute("UPDATE transactions SET status = %s WHERE order_id = %s", (final_status, order_id))
        
        if final_status == 'success':
            c.execute("SELECT username FROM transactions WHERE order_id = %s", (order_id,))
            trx = c.fetchone()
            if trx:
                username_trx = trx[0]
                plan_name = 'professional'
                c.execute("UPDATE users SET plan = %s WHERE username = %s", (plan_name, username_trx))
                print(f"🎉 User {username_trx} di-upgrade ke {plan_name}!")
        
        conn.commit()
        conn.close()

        return jsonify({'status': 'ok'})

    except Exception as e:
        print(f"❌ Error Notification: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("=" * 60)
    print("🔥 FIREVISION SERVER (Refactored for Multi-Session)")
    print("=" * 60)
    
    load_model()
    
    print("\nMenunggu koneksi...")
    app.run(host='0.0.0.0', port=5001, debug=False, threaded=True)

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

app = Flask(__name__)

CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Dictionary untuk menyimpan state per sesi (per kamera)
# Format key: session_id
# Value: {
#   "camera": cv2.VideoCapture object,
#   "is_detecting": bool,
#   "settings": dict,
#   "last_boxes": [],
#   "last_frame_w": 0,
#   "last_frame_h": 0,
#   "fire_was_detected": bool,
#   "frame_counter": 0
# }
sessions = {}

# Model global (bisa dishare karena thread-safe untuk predict)
model = None

try:
    # Notifier instance global, tapi bisa juga per sesi kalau mau chat_id beda
    # Disini kita pakai satu bot telegram buat semua alert
    notifier = TelegramNotifier(
        token="8092461515:AAH1mB855P5-joxZ-eZQ3dBNKmqvO9yipSc",  
        chat_id="1805496530",                                    
    )
    print("✅ Telegram Notifier aktif (hardcode)")
except Exception as e:
    notifier = None
    print(f"⚠️ Telegram Notifier tidak aktif: {e}")


def load_model():
    """Load model YOLO yang sudah dilatih"""
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
    """Fungsi deteksi api menggunakan YOLOv8 per sesi"""
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
    """
    Generator stream video per sesi.
    """
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

            # Pass session object to detect_fire to manage counter & settings
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

            # Logic Notifikasi (Telegram)
            if notifier is not None:
                if fire_detected and not session["fire_was_detected"]:
                    session["fire_was_detected"] = True
                    try:
                        notifier.send_notification(
                            f"🔥 FireVision Alert (Cam {session_id[:4]}) — Api terdeteksi!",
                            frame=processed_frame
                        )
                        print("📨 Telegram alert sent.")
                    except Exception as e:
                        print("❌ Gagal kirim Telegram:", e)

                elif not fire_detected and session["fire_was_detected"]:
                    session["fire_was_detected"] = False
                    try:
                        notifier.send_notification(
                            f"✅ Api telah padam (Cam {session_id[:4]}) — kondisi aman."
                        )
                        print("📨 Telegram cleared sent.")
                    except Exception as e:
                        print("❌ Gagal kirim Telegram:", e)

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
    """
    Endpoint untuk menyalakan kamera baru. 
    Akan membuat session baru setiap kali dipanggil.
    """
    global model, sessions
    
    try:
        if model is None:
            print("Loading YOLO model...")
            if not load_model():
                return jsonify({'error': 'Failed to load model best.pt'}), 500
        
        data = request.get_json() or {}

        camera_source = str(data.get('camera_source', 'WEBCAM')).upper()
        # Jika camera_source IPHONE/IP_CAMERA, user wajib kirim ip_camera_url
        ip_camera_url = data.get('ip_camera_url') 

        # Setup settings awal
        initial_settings = {
            "sensitivity": data.get("sensitivity", 70),
            "camera_source": camera_source,
            "ip_camera_url": ip_camera_url,
            "smoothing": data.get("smoothing", False),
            "noiseReduction": data.get("noiseReduction", False),
            "playbackControls": data.get("playbackControls", False),
        }
        
        # Buat Session ID Baru
        session_id_str = str(uuid.uuid4())
        
        print(f"📷 Request Start Camera. Source: {camera_source}")

        camera_obj = None

        if camera_source == 'IPHONE' or camera_source == 'IP_CAMERA':
            if not ip_camera_url:
                # Default fallback for convenience if needed, but better to require it
                # ip_camera_url = "http://192.168.1.X:8080/video"
                return jsonify({'error': 'URL IP Camera kosong!'}), 400
            
            print(f"Connecting to IP Camera at: {ip_camera_url}")
            camera_obj = cv2.VideoCapture(ip_camera_url)
            camera_obj.set(cv2.CAP_PROP_BUFFERSIZE, 1)

            if not camera_obj.isOpened():
                print("Kamera IP gagal dibuka, coba lagi...")
                time.sleep(1)
                camera_obj = cv2.VideoCapture(ip_camera_url)
        
        else:
            # WEBCAM
            # Boleh terima parameter 'camera_index' kalau user punya banyak webcam USB
            cam_idx = data.get('camera_index', 0)
            print(f"Connecting to Webcam (Index {cam_idx})...")
            camera_obj = cv2.VideoCapture(cam_idx, cv2.CAP_DSHOW)
            if not camera_obj.isOpened():
                print(f"Index {cam_idx} gagal, mencoba fallback ke 0...")
                camera_obj = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        if not camera_obj or not camera_obj.isOpened():
            print("❌ GAGAL: Kamera tidak bisa dibuka.")
            return jsonify({'error': 'Failed to open camera. Check connection/URL.'}), 500

        # Simpan ke dictionary sessions
        sessions[session_id_str] = {
            "camera": camera_obj,
            "is_detecting": True,
            "settings": initial_settings,
            "last_boxes": [],
            "last_frame_w": 0,
            "last_frame_h": 0,
            "fire_was_detected": False,
            "frame_counter": 0
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
    """
    Update setting untuk session tertentu.
    User harus kirim session_id di body/params, kalau tidak update mana?
    Disini kita coba support parameter 'session_id' di body json.
    """
    global sessions
    data = request.get_json() or {}
    
    # Kalau client lama (single cam) gak kirim session_id, kita bisa asumsi update semua session?
    # Atau ambil session pertama. Aman-nya, client harus kirim session_id.
    target_session_id = data.get('session_id')
    
    if target_session_id:
        # Update spesifik
        if target_session_id in sessions:
            settings = sessions[target_session_id]["settings"]
            if 'sensitivity' in data: settings['sensitivity'] = data['sensitivity']
            if 'smoothing' in data: settings['smoothing'] = data['smoothing']
            if 'noiseReduction' in data: settings['noiseReduction'] = data['noiseReduction']
            return jsonify({'status': 'updated', 'session_id': target_session_id})
        else:
            return jsonify({'error': 'Session not found'}), 404
    else:
        # Update semua session (misal global setting)
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
            time.sleep(0.5) # Tunggu loop berhenti
            if session["camera"]:
                session["camera"].release()
            del sessions[target_session_id]
            print(f"🛑 Session stopped: {target_session_id}")
            return jsonify({'status': 'stopped', 'session_id': target_session_id})
        else:
            return jsonify({'status': 'not_found_or_already_stopped'})
    else:
        # Stop All
        # Hanya stop all jika ada flag khusus, untuk mencegah legacy code mematian semua
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
            # Jika tidak ada session_id dan tidak ada flag stop_all, jangan lakukan apa-apa
            # Ini untuk backward compatibility biar DemoFire.vue lama gak matikan semua sesi
            print("⚠️ Warning: stop-detection called without session_id. Ignoring to prevent stopping all sessions.")
            return jsonify({'status': 'ignored_missing_session_id'}), 200

@app.route('/api/video-feed')
def video_feed():
    """Route ini yang dipanggil oleh tag <img src=...> di Vue"""
    session_id = request.args.get('session')
    if not session_id:
        return "Missing session parameter", 400
    
    return Response(
        generate_frames(session_id), 
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'running',
        'active_sessions': len(sessions)
    })


@app.route('/api/detections', methods=['GET'])
def get_detections():
    """
    Endpoint deteksi JSON. Butuh parameter ?session=...
    """
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
    """
    Endpoint untuk deteksi dari 1 gambar upload (tidak butuh session).
    """
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

        # Kita buat dummy session data buat detect_fire
        dummy_session = {
            "settings": {"sensitivity": sensitivity},
            "frame_counter": 0
        }
        
        processed_frame, fire_detected, detections = detect_fire(frame, dummy_session)

        # Bisa kirim telegram juga
        if fire_detected and notifier is not None:
             # ... (Opsional: kirim notif untuk single upload)
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
    app.run(host='0.0.0.0', port=5001, debug=True, threaded=True)

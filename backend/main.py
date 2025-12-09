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
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})

camera = None
is_detecting = False
detection_settings = {}
session_id = None
model = None
frame_counter = 0            
last_processed_frame = None  


last_boxes = []              
last_frame_w = 0
last_frame_h = 0

fire_was_detected = False

DEFAULT_IP_CAMERA_URL = "http://192.168.110.160:4747/video"

try:
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


def detect_fire(frame, sensitivity=70):
    """Fungsi deteksi api menggunakan YOLOv8"""
    global model, frame_counter
    
    if model is None:
        return frame, False, []
    
    conf_threshold = sensitivity / 100.0
    
    results = model(frame, conf=conf_threshold, verbose=False)
    
    fire_detected = False
    detections = []
    
    blink_speed = 2
    alpha = (math.sin(frame_counter * blink_speed * 0.1) + 1) / 2
    alpha = 0.5 + (alpha * 0.5)
    frame_counter += 1
    
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


def generate_frames():
    """
    Generator stream video untuk dikirim ke Browser.
    Versi ini TIDAK lagi reuse frame lama, jadi tampilan di frontend lebih halus.
    YOLO dijalankan di setiap frame (kalau PC agak kuat, ini oke).
    """
    global camera, is_detecting, detection_settings
    global last_boxes, last_frame_w, last_frame_h
    global fire_was_detected, notifier

    while is_detecting:
        if camera is None:
            break

        success, frame = camera.read()
        if not success:
            time.sleep(0.05)
            continue

        try:
            frame = cv2.resize(frame, (640, 480))

            sensitivity = detection_settings.get("sensitivity", 70)

            processed_frame, fire_detected, detections = detect_fire(frame, sensitivity)

            h, w = processed_frame.shape[:2]
            last_frame_w = w
            last_frame_h = h

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
            last_boxes = boxes_for_api

            if notifier is not None:
                if fire_detected and not fire_was_detected:
                    fire_was_detected = True
                    try:
                        notifier.send_notification(
                            "🔥 FireVision Alert — Api terdeteksi dari kamera!",
                            frame=processed_frame
                        )
                        print("📨 Telegram alert sent.")
                    except Exception as e:
                        print("❌ Gagal kirim Telegram:", e)

                elif not fire_detected and fire_was_detected:
                    fire_was_detected = False
                    try:
                        notifier.send_notification(
                            "✅ Api telah padam — kondisi aman."
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
            print(f"Error inside video loop: {e}")
            break



@app.route('/')
def index():
    return jsonify({'status': 'running', 'message': 'FireVision API is Online'})


@app.route('/api/start-detection', methods=['POST'])
def start_detection():
    """
    Endpoint untuk menyalakan kamera (Webcam atau IP Camera)
    - camera_source: "WEBCAM" | "IPHONE"
    - ip_camera_url: URL stream kalau IPHONE
    """
    global camera, is_detecting, detection_settings, session_id, model, last_processed_frame
    
    try:
        if model is None:
            print("Loading YOLO model...")
            if not load_model():
                return jsonify({'error': 'Failed to load model best.pt'}), 500
        
        last_processed_frame = None

        data = request.get_json() or {}

        camera_source = str(data.get('camera_source', 'WEBCAM')).upper()
        ip_camera_url = data.get('ip_camera_url') or DEFAULT_IP_CAMERA_URL

        detection_settings = {
            "sensitivity": data.get("sensitivity", 70),
            "camera_source": camera_source,
            "ip_camera_url": ip_camera_url,
            "smoothing": data.get("smoothing", False),
            "noiseReduction": data.get("noiseReduction", False),
            "playbackControls": data.get("playbackControls", False),
        }
        
        session_id_str = str(uuid.uuid4())
        globals()["session_id"] = session_id_str

        if camera is not None:
            try:
                camera.release()
            except:
                pass
            camera = None

        print(f"📷 Request Start Camera. Source: {camera_source}")

        if camera_source == 'IPHONE':
            if not ip_camera_url:
                return jsonify({'error': 'URL IP Camera kosong!'}), 400
            
            print(f"Connecting to IP Camera at: {ip_camera_url}")
            camera_obj = cv2.VideoCapture(ip_camera_url)
            camera_obj.set(cv2.CAP_PROP_BUFFERSIZE, 1)

            if not camera_obj.isOpened():
                print("Kamera IP belum terbuka, mencoba lagi...")
                time.sleep(2)
                camera_obj = cv2.VideoCapture(ip_camera_url)
                camera_obj.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        else:
            print("Connecting to Webcam (Index 0)...")
            camera_obj = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            if not camera_obj.isOpened():
                print("Index 0 gagal, mencoba Index 1...")
                camera_obj = cv2.VideoCapture(1, cv2.CAP_DSHOW)

        if not camera_obj or not camera_obj.isOpened():
            print("❌ GAGAL: Kamera tidak bisa dibuka.")
            return jsonify({'error': 'Failed to open camera. Check connection.'}), 500

        globals()["camera"] = camera_obj
        globals()["is_detecting"] = True

        print(f"✅ Camera Started! Session: {session_id_str}")
        
        return jsonify({
            'status': 'started',
            'session_id': session_id_str,
            'camera_source': camera_source
        })
        
    except Exception as e:
        print(f"Error starting detection: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/update-settings', methods=['POST'])
def update_settings():
    global detection_settings
    data = request.get_json() or {}
    
    # Update sensitivity if present
    if 'sensitivity' in data:
        detection_settings['sensitivity'] = data['sensitivity']
        print(f"⚙️ Sensitivity updated to: {data['sensitivity']}")
        
    # Update other settings if needed
    if 'smoothing' in data:
        detection_settings['smoothing'] = data['smoothing']
        
    if 'noiseReduction' in data:
        detection_settings['noiseReduction'] = data['noiseReduction']
        
    return jsonify({'status': 'updated', 'settings': detection_settings})


@app.route('/api/stop-detection', methods=['POST'])
def stop_detection():
    global camera, is_detecting, session_id
    print("🛑 Stopping detection...")
    is_detecting = False
    
    time.sleep(0.5)
    
    if camera is not None:
        try:
            camera.release()
        except:
            pass
        camera = None
    
    session_id = None
    return jsonify({'status': 'stopped'})


@app.route('/api/video-feed')
def video_feed():
    """Route ini yang dipanggil oleh tag <img src=...> di Vue"""
    return Response(
        generate_frames(), 
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'running',
        'camera_active': camera is not None and camera.isOpened() if camera else False
    })


@app.route('/api/detections', methods=['GET'])
def get_detections():
    """
    Endpoint yang dipanggil DemoFire.vue untuk menampilkan bounding box live.
    Tidak pakai session_id secara ketat, hanya mengembalikan deteksi terakhir.
    """
    global last_boxes, last_frame_w, last_frame_h
    return jsonify({
        "boxes": last_boxes,
        "frame_w": last_frame_w,
        "frame_h": last_frame_h,
    })



@app.route('/api/detect', methods=['POST'])
def detect_single_frame():
    """
    Endpoint untuk deteksi dari 1 gambar yang dikirim browser.
    Browser akan upload frame (jpeg/png) lewat FormData (field: file).
    """
    global model, notifier

    print("=== /api/detect dipanggil ===")
    print("Content-Type:", request.content_type)
    print("request.files keys:", list(request.files.keys()))
    print("request.form keys:", list(request.form.keys()))

    if model is None:
        print("Model belum di-load, mencoba load...")
        if not load_model():
            return jsonify({'error': 'Model not loaded'}), 500

    file = request.files.get('file')
    if file is None:
        print("Tidak ada field 'file' di request.files")
        return jsonify({'error': "No file field named 'file'"}), 400

    if file.filename == '':
        print("Field 'file' ada tapi filename kosong")
        return jsonify({'error': 'No selected file'}), 400

    try:
        raw = file.read()
        print("Ukuran raw bytes:", len(raw))

        file_bytes = np.frombuffer(raw, np.uint8)
        frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        if frame is None:
            print("cv2.imdecode mengembalikan None (bukan gambar valid)")
            return jsonify({'error': 'Failed to decode image'}), 400

        try:
            sensitivity = int(request.form.get('sensitivity', 70))
        except:
            sensitivity = 70

        print("Sensitivitas:", sensitivity)

        processed_frame, fire_detected, detections = detect_fire(frame, sensitivity)

        if fire_detected and notifier is not None:
            try:
                notifier.send_notification(
                    "🔥 FireVision Alert — Api terdeteksi dari gambar upload!",
                    frame=processed_frame
                )
                print("📨 Telegram alert (single frame) sent.")
            except Exception as e:
                print("❌ Gagal kirim Telegram (single frame):", e)

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
    print("🔥 FIREVISION SERVER (YOLO + FLASK)")
    print("=" * 60)
    
    load_model()
    
    print("\nMenunggu koneksi dari Vue...")
    app.run(host='0.0.0.0', port=5001, debug=True, threaded=True)

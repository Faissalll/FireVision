from flask import Blueprint, request, jsonify, Response, current_app
import cv2
import uuid
import time
import os
from ..utils.decorators import token_required
from ..services.detector import load_model, generate_frames, sessions, model
from ..services import detector
# from ..database import get_db_connection (Removed for Microservice)

stream_bp = Blueprint('stream', __name__, url_prefix='/api')

@stream_bp.route('/start-detection', methods=['POST'])
@token_required
def start_detection(current_user):
    try:
        print("[START_DETECTION] Triggered for user:", current_user)
        
        if detector.model is None:
            print("[START_DETECTION] Loading YOLO model...")
            if not detector.load_model():
                print("[START_DETECTION] ERROR: Failed to load model")
                return jsonify({'error': 'Failed to load model best.pt'}), 500
        
        data = request.get_json() or {}
        username = current_user
        if not username:
            print("[START_DETECTION] ERROR: No username")
            return jsonify({'error': 'Username required'}), 400

        camera_source = str(data.get('camera_source', 'WEBCAM')).upper()
        ip_camera_url = data.get('ip_camera_url') 
        
        print(f"[START_DETECTION] Camera source: {camera_source}, IP URL: {ip_camera_url}")
        
        # Init Settings
        initial_settings = {
            "sensitivity": data.get("sensitivity", 70),
            "camera_source": camera_source,
            "ip_camera_url": ip_camera_url,
            "smoothing": data.get("smoothing", False),
            "noiseReduction": data.get("noiseReduction", False),
            "playbackControls": data.get("playbackControls", False),
        }
        
        # Init Camera
        camera_obj = None
        if camera_source in ['IPHONE', 'IP_CAMERA']:
            if not ip_camera_url:
                print("[START_DETECTION] ERROR: IP Camera URL empty")
                return jsonify({'error': 'URL IP Camera kosong!'}), 400
            try:
                print(f"[START_DETECTION] Opening IP camera: {ip_camera_url}")
                camera_obj = cv2.VideoCapture(ip_camera_url)
                if not camera_obj.isOpened():
                    print("[START_DETECTION] First attempt failed, retrying...")
                    time.sleep(1)
                    camera_obj = cv2.VideoCapture(ip_camera_url)
            except Exception as e:
                print(f"[START_DETECTION] Error opening IP cam: {e}")
                return jsonify({'error': f'Failed to open IP camera: {str(e)}'}), 500
        else:
            # Webcam - will likely fail on cloud
            try:
                cam_idx = int(data.get('camera_index', 0))
                print(f"[START_DETECTION] Opening webcam index: {cam_idx}")
                camera_obj = cv2.VideoCapture(cam_idx)
                if not camera_obj.isOpened():
                    print("[START_DETECTION] Webcam 0 failed, trying default...")
                    camera_obj = cv2.VideoCapture(0)
            except Exception as e:
                print(f"[START_DETECTION] Error opening webcam: {e}")
                return jsonify({'error': f'Failed to open webcam: {str(e)}'}), 500
                
        # Critical Check
        if camera_obj is None or not camera_obj.isOpened():
            print("[START_DETECTION] ERROR: Camera not opened")
            return jsonify({'error': 'Server Cloud cannot access local webcam. Use IP Camera.'}), 500

        # Start Session
        session_id_str = str(uuid.uuid4())
        detector.sessions[session_id_str] = {
            "camera": camera_obj,
            "is_detecting": True,
            "settings": initial_settings,
            "last_boxes": [],
            "last_frame_w": 0,
            "last_frame_h": 0,
            "notification_settings": {"telegram_enabled": True, "email_enabled": True}, 
            "fire_was_detected": False,
            "frame_counter": 0,
            "owner": username,
            "camera_name": data.get('camera_name', 'Camera')
        }

        print(f"[START_DETECTION] SUCCESS: Session created: {session_id_str}")
        return jsonify({'status': 'started', 'session_id': session_id_str})

    except Exception as e:
        print(f"[START_DETECTION] EXCEPTION: {type(e).__name__}: {e}")
        return jsonify({'error': f'Internal error: {str(e)}'}), 500

@stream_bp.route('/stop-detection', methods=['POST'])
@token_required
def stop_detection(current_user):
    data = request.get_json() or {}
    target_session_id = data.get('session_id')

    if target_session_id:
        if target_session_id in detector.sessions:
            session = detector.sessions[target_session_id]
            session["is_detecting"] = False
            time.sleep(0.5) 
            if session["camera"]:
                session["camera"].release()
            del detector.sessions[target_session_id]
            print(f"🛑 Session stopped: {target_session_id}")
            return jsonify({'status': 'stopped', 'session_id': target_session_id})
        else:
            return jsonify({'status': 'not_found_or_already_stopped'})
    else:
        if data.get('stop_all') is True:
            print("🛑 Stopping ALL sessions...")
            ids = list(detector.sessions.keys())
            for sid in ids:
                detector.sessions[sid]["is_detecting"] = False
                if detector.sessions[sid]["camera"]:
                    detector.sessions[sid]["camera"].release()
            detector.sessions.clear()
            return jsonify({'status': 'stopped_all'})
        else:
            return jsonify({'status': 'ignored_missing_session_id'}), 200

@stream_bp.route('/video-feed')
def video_feed():
    session_id = request.args.get('session')
    if not session_id:
        return "Missing session parameter", 400
    
    return Response(
        generate_frames(session_id), 
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@stream_bp.route('/process-frame', methods=['POST'])
@token_required
def process_frame(current_user):
    """
    Process a single frame from browser webcam.
    Accepts: multipart/form-data with 'frame' file or JSON with 'frame' as base64
    Returns: JSON with detections
    """
    try:
        import base64
        import numpy as np
        
        # Load model if not loaded
        if detector.model is None:
            print("[PROCESS_FRAME] Loading YOLO model...")
            if not detector.load_model():
                return jsonify({'error': 'Failed to load model'}), 500
        
        frame = None
        sensitivity = 70
        
        # Try to get frame from form data (file upload)
        if 'frame' in request.files:
            file = request.files['frame']
            file_bytes = np.frombuffer(file.read(), np.uint8)
            frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            sensitivity = int(request.form.get('sensitivity', 70))
        
        # Try to get frame from JSON (base64)
        elif request.is_json:
            data = request.get_json()
            if 'frame' in data:
                # Remove data URL prefix if present
                frame_data = data['frame']
                if ',' in frame_data:
                    frame_data = frame_data.split(',')[1]
                
                frame_bytes = base64.b64decode(frame_data)
                nparr = np.frombuffer(frame_bytes, np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                sensitivity = int(data.get('sensitivity', 70))
        
        if frame is None:
            return jsonify({'error': 'No frame provided'}), 400
        
        # Run detection
        conf_threshold = sensitivity / 100.0
        results = detector.model(frame, conf=conf_threshold, verbose=False)
        
        detections = []
        fire_detected = False
        
        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                
                confidence = float(box.conf[0])
                class_id = int(box.cls[0])
                
                if hasattr(detector.model, "names"):
                    class_name = detector.model.names[class_id]
                else:
                    class_name = str(class_id)
                
                if class_name.lower() in ['fire', 'smoke']:
                    fire_detected = True
                
                detections.append({
                    "class": class_name,
                    "confidence": confidence,
                    "x": x1,
                    "y": y1,
                    "w": x2 - x1,
                    "h": y2 - y1
                })
        
        return jsonify({
            'success': True,
            'fire_detected': fire_detected,
            'detections': detections,
            'frame_width': frame.shape[1],
            'frame_height': frame.shape[0]
        })
        
    except Exception as e:
        print(f"[PROCESS_FRAME] ERROR: {e}")
        return jsonify({'error': str(e)}), 500

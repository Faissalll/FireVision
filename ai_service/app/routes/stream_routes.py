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
    print("🚀 Start Detection Triggered")
    try:
        if detector.model is None:
            print("Loading YOLO model...")
            if not detector.load_model():
                return jsonify({'error': 'Failed to load model best.pt'}), 500
        
        data = request.get_json() or {}
        username = current_user
        if not username:
             return jsonify({'error': 'Username required'}), 400

        # Enforce Camera Limits (Simplification: AI Service trusts Backend)
        # We skip DB checks here because AI Service is decoupled.
        # Ideally backend checks limit before calling this, or we call backend API.
        
        active_count = 0
        for s_id, s_data in detector.sessions.items():
            if s_data.get('owner') == username and s_data.get('is_detecting'):
                active_count += 1
        
        # Mock Plan Check (Assume Premium for now or rely on Backend to cut off)
        # To strictly enforce, we would need to call Backend API.
        # For this MVP, we relax the check to avoid 'mysql' dependnecy.
        # user_plan = ... 

        # Mock Notification Settings (Or fetch via Backend API if critical)
        notif_settings = {
             "telegram_enabled": True, # Default to True if configured in Env
             "email_enabled": True
        }
        
        # ... logic continues ...

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
            # Convert to int if possible
            try: cam_idx = int(cam_idx)
            except: pass
            
            # CLOUD COMPATIBILITY FIX:
            # 1. Remove cv2.CAP_DSHOW (Windows only, crashes on Linux/Cloud)
            # 2. Add fallback/error handling for cloud servers with no webcam
            
            try:
                # Try default backend first
                camera_obj = cv2.VideoCapture(cam_idx)
                
                if not camera_obj.isOpened():
                    print(f"Index {cam_idx} gagal opened, trying index 0...")
                    camera_obj = cv2.VideoCapture(0)
            except Exception as e:
                print(f"Error opening webcam: {e}")
                camera_obj = None

        if not camera_obj or not camera_obj.isOpened():
            print("❌ GAGAL: Kamera tidak bisa dibuka.")
            return jsonify({
                'error': 'Server Cloud cannot access local webcam. Please use IP Camera option.'
            }), 500

        detector.sessions[session_id_str] = {
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
            "camera_name": camera_name_custom
        }

        print(f"✅ Camera Session Started! ID: {session_id_str}")
        
        return jsonify({
            'status': 'started',
            'session_id': session_id_str
        })
        
    except Exception as e:
        print(f"Error starting detection: {e}")
        return jsonify({'error': str(e)}), 500
        
    # Safety net for any control flow fall-through
    return jsonify({'error': 'Unexpected Server Error (Fallthrough)'}), 500

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

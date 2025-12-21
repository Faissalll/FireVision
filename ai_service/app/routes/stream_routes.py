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

        camera_source = str(data.get('camera_source', 'WEBCAM')).upper()
        ip_camera_url = data.get('ip_camera_url') 
        
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
                return jsonify({'error': 'URL IP Camera kosong!'}), 400
            try:
                camera_obj = cv2.VideoCapture(ip_camera_url)
                if not camera_obj.isOpened():
                    time.sleep(1)
                    camera_obj = cv2.VideoCapture(ip_camera_url)
            except Exception as e:
                print(f"Error opening IP cam: {e}")
        else:
            # Webcam Fallback Logic
            try:
                cam_idx = int(data.get('camera_index', 0))
                camera_obj = cv2.VideoCapture(cam_idx)
                if not camera_obj.isOpened():
                    camera_obj = cv2.VideoCapture(0)
            except Exception as e:
                print(f"Error opening webcam: {e}")
                
        # Critical Check
        if not camera_obj or not camera_obj.isOpened():
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

        return jsonify({'status': 'started', 'session_id': session_id_str})

    except Exception as e:
        print(f"Error starting detection: {e}")
        return jsonify({'error': str(e)}), 500
    
    # Ultimate Safety Net (Should be unreachable if all paths above return)
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

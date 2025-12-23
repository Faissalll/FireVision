from flask import Blueprint, request, jsonify
from ..utils.decorators import token_required
from ..database import get_db_connection
from ..services import detector

user_bp = Blueprint('user', __name__, url_prefix='/api')

@user_bp.route('/profile', methods=['GET', 'PUT'])
@token_required
def profile_api(current_user):
    username = current_user
    conn = get_db_connection()
    c = conn.cursor(dictionary=True)

    if request.method == 'GET':
        try:
            c.execute("SELECT id, username, plan FROM users WHERE username = %s", (username,))
            user = c.fetchone()
            if not user:
                return jsonify({'error': 'User not found'}), 404
            return jsonify(user)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            conn.close()

    elif request.method == 'PUT':
        data = request.get_json() or {}
        new_username = data.get('username')
        
        # NOTE: Password change should ideally be a separate endpoint for security (requiring old password),
        # but for this request we focus on Profile Sync (username/basic info).
        
        if not new_username:
             return jsonify({'error': 'Username cannot be empty'}), 400
             
        try:
            # Check if username exists (if changing)
            if new_username != username:
                c.execute("SELECT id FROM users WHERE username = %s", (new_username,))
                if c.fetchone():
                     return jsonify({'error': 'Username already taken'}), 409
            
            c.execute("UPDATE users SET username = %s WHERE username = %s", (new_username, username))
            # If we had other fields like email/fullname, update them here too.
            
            # Create new token since username (identity) changed? 
            # ideally yes, but for simplicity let's return success and let frontend handle re-login or state update.
            # Actually, if we change username, the current token (containing old username) becomes invalid for future requests 
            # that rely on looking up the user by the token's username payload.
            # SO: We must issue a new token or warn the user.
            
            conn.commit()
            
            return jsonify({
                'status': 'success', 
                'message': 'Profile updated',
                'username': new_username,
                'note': 'If username changed, please re-login.'
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            conn.close()

@user_bp.route('/notification-settings', methods=['GET', 'POST'])
@token_required
def notification_settings_api(current_user):
    data = request.get_json(silent=True) or {}
    username = current_user 

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
            
            # Update active sessions for this user
            for sid, s in detector.sessions.items():
                if s.get('owner') == username:
                    # We need a new cursor for this check or reuse? Better create new.
                    # Wait, we are already inside a function with connection 'conn'
                    # Reuse 'conn' for this fetch
                    c.execute("SELECT * FROM notification_settings WHERE username = %s", (username,))
                    s['notification_settings'] = c.fetchone()
                    print(f"🔄 Updated live settings for session {sid}")

            return jsonify({'status': 'saved'})
        except Exception as e:
            print(f"Error saving settings: {e}")
            return jsonify({'error': str(e)}), 500
        finally:
            if conn.is_connected():
                conn.close()

@user_bp.route('/update-settings', methods=['POST'])
@token_required
def update_settings(current_user):
    data = request.get_json() or {}
    
    target_session_id = data.get('session_id')
    
    if target_session_id:
        if target_session_id in detector.sessions:
            settings = detector.sessions[target_session_id]["settings"]
            if 'sensitivity' in data: settings['sensitivity'] = data['sensitivity']
            if 'smoothing' in data: settings['smoothing'] = data['smoothing']
            if 'noiseReduction' in data: settings['noiseReduction'] = data['noiseReduction']
            return jsonify({'status': 'updated', 'session_id': target_session_id})
        else:
            return jsonify({'error': 'Session not found'}), 404
    else:
        for sid in detector.sessions:
            settings = detector.sessions[sid]["settings"]
            if 'sensitivity' in data: settings['sensitivity'] = data['sensitivity']
            if 'smoothing' in data: settings['smoothing'] = data['smoothing']
            if 'noiseReduction' in data: settings['noiseReduction'] = data['noiseReduction']
        return jsonify({'status': 'updated_all'})

@user_bp.route('/add-alarm', methods=['POST'])
def add_alarm():
    """Add new alarm record from frontend detection"""
    print("🚨 POST /api/add-alarm called")
    
    try:
        data = request.get_json() or {}
        
        # Get alarm data from request
        camera_id = data.get('camera_id', 'Unknown Camera')
        confidence = float(data.get('confidence', 0))
        zone = data.get('zone', 'Default Zone')
        timestamp = data.get('timestamp', '')
        
        # Generate UUID for this alarm
        import uuid
        from datetime import datetime
        
        alarm_uuid = str(uuid.uuid4())
        if not timestamp:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        conn = get_db_connection()
        if not conn:
            print("❌ DB connection failed")
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO alarms (uuid, timestamp, camera_id, zone, confidence, status, image_path)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            alarm_uuid,
            timestamp,
            camera_id,
            zone,
            confidence,
            'active',
            ''
        ))
        
        conn.commit()
        alarm_id = cursor.lastrowid
        conn.close()
        
        print(f"💾 Alarm saved: ID={alarm_id}, UUID={alarm_uuid}, Camera={camera_id}, Confidence={confidence}")
        
        return jsonify({
            'success': True,
            'alarm_id': alarm_id,
            'uuid': alarm_uuid
        })
        
    except Exception as e:
        print(f"❌ Error saving alarm: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/history', methods=['GET'])
def get_history():
    """Ultra-simplified history endpoint - guaranteed to return valid response"""
    print("🚀 GET /api/history called")
    
    # Always return a valid response, even if DB fails
    try:
        conn = get_db_connection()
        print(f"📍 Connection result: {conn}")
        
        if not conn:
            print("❌ No DB connection - returning empty array")
            return jsonify([])  # Return empty array instead of error
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM alarms ORDER BY id DESC LIMIT 100")
        rows = cursor.fetchall() or []
        conn.close()
        
        print(f"✅ Found {len(rows)} alarms")
        
        result = []
        for row in rows:
            result.append({
                "id": f"ALM-{row.get('id', 0):03d}",
                "db_id": row.get('id', 0),
                "uuid": str(row.get('uuid', '')),
                "time": "",
                "date": "",
                "camera": str(row.get('camera_id', '')),
                "zone": str(row.get('zone', '')),
                "confidence": float(row.get('confidence', 0) or 0),
                "status": str(row.get('status', 'Unverified')),
                "image": str(row.get('image_path', ''))
            })
        
        print(f"✅ Returning {len(result)} items")
        return jsonify(result)
        
    except Exception as e:
        print(f"❌ Exception: {e}")
        return jsonify([])  # Return empty array on any error

@user_bp.route('/history/update-status', methods=['POST'])
def update_history_status():
    data = request.get_json()
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
        return jsonify({'status': 'success', 'message': 'Status updated'})
    except Exception as e:
        print(f"Error update history: {e}")
        return jsonify({'error': str(e)}), 500

@user_bp.route('/telegram/get-chat-id', methods=['POST'])
@token_required
def get_telegram_chat_id(current_user):
    data = request.get_json() or {}
    token = data.get('token')
    
    if not token:
        return jsonify({'error': 'Bot Token Required'}), 400
        
    try:
        import requests
        # Call getUpdates
        url = f"https://api.telegram.org/bot{token}/getUpdates"
        r = requests.get(url, timeout=10)
        data = r.json()
        
        if not data.get('ok'):
             return jsonify({'error': f"Telegram API Error: {data.get('description')}"}), 400
             
        result = data.get('result', [])
        if not result:
            return jsonify({'error': 'Belum ada pesan masuk. Silakan kirim "Halo" ke bot Anda.'}), 404
            
        # Get latest message
        latest = result[-1]
        chat_id = latest.get('message', {}).get('chat', {}).get('id')
        
        if not chat_id:
             # Try edited_message or other types
             chat_id = latest.get('my_chat_member', {}).get('chat', {}).get('id')
        
        if chat_id:
            return jsonify({'chat_id': str(chat_id)})
        else:
            return jsonify({'error': 'Tidak dapat menemukan Chat ID dalam update terakhir.'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

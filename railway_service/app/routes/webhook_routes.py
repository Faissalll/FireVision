from flask import Blueprint, request, jsonify
from ..services.email_notifier import EmailNotifier
from ..services.telegram_notifier import TelegramNotifier
from ..database import get_db_connection
import os

webhook_bp = Blueprint('webhook', __name__, url_prefix='/api/webhook')

WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', 'rahasia123')

@webhook_bp.route('/fire-alert', methods=['POST'])
def receive_fire_alert():
    # 1. Security Check
    secret = request.headers.get('X-Webhook-Secret')
    if secret != WEBHOOK_SECRET:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json() or {}
    print(f"🔥 RECEIVED FIRE ALERT: {data}")

    # Data Structure expected:
    # {
    #    "users": ["admin", "user1"], 
    #    "image_url": "http://...", 
    #    "timestamp": "..."
    #    "confidence": 0.95
    # }

    # For now, we iterate all users (since current system broadcasts, 
    # or we can look up settings for specific active users if passed).
    # Since AI Service doesn't know "User Config", it just sends "Fire Detected".
    # Backend (this service) MUST look up who to notify.
    
    # PROBLEM: Backend doesn't know which SESSION detected fire unless AI sends session_id.
    # Let's assume AI sends session_id or username.
    
    target_username = data.get('username')
    
    if not target_username:
        # Broadcast to all? Or just log?
        return jsonify({'status': 'ignored', 'reason': 'no_username'}), 400
        
    try:
        conn = get_db_connection()
        c = conn.cursor(dictionary=True)
        c.execute("SELECT * FROM notification_settings WHERE username = %s", (target_username,))
        settings = c.fetchone()
        conn.close()
        
        if not settings:
             return jsonify({'status': 'no_settings_found'})

        # Notify Telegram
        if settings.get('telegram_enabled') and settings.get('telegram_bot_token') and settings.get('telegram_chat_id'):
            try:
                tn = TelegramNotifier(settings['telegram_bot_token'], settings['telegram_chat_id'])
                msg = f"🔥 API TERDETEKSI! \nConfidence: {data.get('confidence')}\nWaktu: {data.get('timestamp')}"
                tn.send_message(msg)
                # If image provided
                if data.get('image_base64'): # If sending raw bytes
                     pass 
                print(f"✅ Telegram sent to {target_username}")
            except Exception as e:
                print(f"❌ Telegram failed: {e}")

        # Notify Email
        if settings.get('email_enabled') and settings.get('email_recipient'):
            try:
                # Setup EmailNotifier (requires logic adaptation)
                pass 
            except Exception as e:
                print(f"❌ Email failed: {e}")

        return jsonify({'status': 'processed'})

    except Exception as e:
        print(f"Webhook Error: {e}")
        return jsonify({'error': str(e)}), 500

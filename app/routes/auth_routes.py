from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import mysql.connector
from ..database import get_db_connection

auth_bp = Blueprint('auth', __name__, url_prefix='/api')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if not username or not password:
        return jsonify({'error': 'Username dan password wajib diisi'}), 400

    hashed_password = generate_password_hash(password)

    try:
        conn = get_db_connection()
        c = conn.cursor()
        # Default plan is 'free'
        # Check if email is provided
        if email:
            c.execute("INSERT INTO users (username, password, email, plan) VALUES (%s, %s, %s, 'free')", (username, hashed_password, email))
        else:
            c.execute("INSERT INTO users (username, password, plan) VALUES (%s, %s, 'free')", (username, hashed_password))
        
        conn.commit()
        conn.close()
        return jsonify({'status': 'success', 'message': 'Registrasi berhasil!'})
    except mysql.connector.Error as err:
        if err.errno == 1062: # Duplicate entry
            # Check which key caused duplicate
            msg = str(err)
            if 'username' in msg:
                return jsonify({'error': 'Username sudah digunakan'}), 409
            if 'email' in msg:
                 return jsonify({'error': 'Email sudah digunakan'}), 409
            return jsonify({'error': 'Username atau Email sudah digunakan'}), 409
        return jsonify({'error': str(err)}), 500
    except Exception as e:
        print(f"Error register: {e}")
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
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
            }, current_app.config['SECRET_KEY'], algorithm="HS256")

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

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json() or {}
    email = data.get('email')
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400
        
    try:
        conn = get_db_connection()
        c = conn.cursor(dictionary=True)
        c.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = c.fetchone()
        
        if not user:
            conn.close()
            # Return success even if not found to prevent user enumeration
            return jsonify({'message': 'Jika email terdaftar, instruksi reset password telah dikirim.'})
            
        # Generate Reset Token
        import uuid
        token = str(uuid.uuid4())
        # Expires in 1 hour
        expiry = (datetime.datetime.now() + datetime.timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')
        
        c.execute("INSERT INTO password_resets (email, token, expires_at) VALUES (%s, %s, %s)", (email, token, expiry))
        conn.commit()
        conn.close()
        
        # Send Email (Mocked or Real)
        # We need to import the Email Notifier service or use simple logic
        # For this refactor, let's try to access the service logic
        from ..services.notifier import EmailNotifier
        
        # Check if we have global email settings in env or use specific system email
        import os
        smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', 587))
        smtp_user = os.getenv('SMTP_USER', '') # System email
        smtp_pass = os.getenv('SMTP_PASS', '') 
        
        if smtp_user and smtp_pass:
             try:
                 en = EmailNotifier(smtp_host, smtp_port, smtp_user, smtp_pass, email)
                 reset_link = f"http://localhost:5173/reset-password?token={token}"
                 en.send_email("Reset Password Request", f"Klik link ini untuk reset password Anda: {reset_link}\\n\\nLink valid selama 1 jam.")
                 print(f"📧 Reset email sent to {email}")
             except Exception as e:
                 print(f"❌ Failed to send email: {e}")
        else:
             print(f"⚠️ SMTP not configured. Mock Reset Token: {token}")
        
        return jsonify({'message': 'Jika email terdaftar, instruksi reset password telah dikirim.', 'mock_token': token}) # Returning mock_token for dev testing
        
    except Exception as e:
        print(f"Error forgot-password: {e}")
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json() or {}
    token = data.get('token')
    new_password = data.get('password')
    
    if not token or not new_password:
        return jsonify({'error': 'Token and new password required'}), 400
        
    try:
        conn = get_db_connection()
        c = conn.cursor(dictionary=True)
        
        # Verify Token
        c.execute("SELECT * FROM password_resets WHERE token = %s AND expires_at > NOW() ORDER BY created_at DESC LIMIT 1", (token,))
        reset_entry = c.fetchone()
        
        if not reset_entry:
            conn.close()
            return jsonify({'error': 'Token invalid or expired'}), 400
            
        email = reset_entry['email']
        
        # Update User Password
        hashed_password = generate_password_hash(new_password)
        c.execute("UPDATE users SET password = %s WHERE email = %s", (hashed_password, email))
        
        # Delete used token (or all tokens for this email)
        c.execute("DELETE FROM password_resets WHERE email = %s", (email,))
        
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Password berhasil direset. Silakan login.'})
        
    except Exception as e:
         print(f"Error reset-password: {e}")
         return jsonify({'error': str(e)}), 500

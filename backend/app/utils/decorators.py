from functools import wraps
from flask import request, jsonify, current_app
import jwt
import os

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
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['username']
        except Exception as e:
            return jsonify({'message': 'Token is invalid!', 'error': str(e)}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

def decode_token(token):
    """Decode JWT token and return username, or None if invalid"""
    from flask import current_app
    try:
        data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        return data.get('username')
    except Exception:
        return None


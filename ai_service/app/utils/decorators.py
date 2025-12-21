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
            print(f"Auth Error: {e}")
            return jsonify({'message': 'Token is invalid!', 'error': str(e)}), 401
        
        print(f"Token Valid for user: {current_user}")
        result = f(current_user, *args, **kwargs)
        if result is None:
            print("❌ Decorated function returned None!")
        return result
    return decorated

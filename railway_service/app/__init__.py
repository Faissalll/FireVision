from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from .database import init_db
from .routes.auth_routes import auth_bp
from .routes.stream_routes import stream_bp
from .routes.user_routes import user_bp

def create_app():
    # Load env manually or via dotenv
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    load_dotenv(env_path)
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'FireVisionSecretKey2025!Secure')
    
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "OPTIONS", "PUT", "DELETE"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Initialize DB (creates tables if needed)
    with app.app_context():
        init_db()
    
    # Imports for blueprints moved inside create_app as per instruction
    from .routes.user_routes import user_bp
    from .routes.webhook_routes import webhook_bp

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(webhook_bp) # Registered webhook_bp
    
    @app.route('/')
    def index():
        return jsonify({'status': 'running', 'message': 'FireVision API is Online (Refactored)'})

    @app.route('/api/health', methods=['GET'])
    def health_check():
        from .services.detector import sessions
        return jsonify({
            'status': 'running',
            'active_sessions': len(sessions)
        })
        
    return app

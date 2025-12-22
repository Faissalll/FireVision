from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
# from .database import init_db
# from .routes.auth_routes import auth_bp
from .routes.stream_routes import stream_bp
# from .routes.user_routes import user_bp

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
    # with app.app_context():
    #     init_db()
    
    # Register Blueprints
    # app.register_blueprint(auth_bp)
    app.register_blueprint(stream_bp)
    # app.register_blueprint(user_bp)
    
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
        
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal Server Error', 'message': str(error)}), 500

    @app.errorhandler(Exception)
    def handle_exception(e):
        # pass through HTTP errors
        if isinstance(e,  (int, str)): 
             return jsonify({'error': str(e)}), 500
        return jsonify({'error': str(e), 'type': type(e).__name__}), 500
        
    return app

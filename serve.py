from app import create_app
from waitress import serve
import os

app = create_app()

# Serve Frontend Static Files
# We need to configure Flask to serve the 'dist' folder from Vue build
# But since our app factory is cleaner, let's just add a route here or modify __init__.py slightly
# A simpler way for this quick deployment:
from flask import send_from_directory

FRONTEND_DIST = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'my-app', 'dist'))

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if path != "" and os.path.exists(os.path.join(FRONTEND_DIST, path)):
        return send_from_directory(FRONTEND_DIST, path)
    else:
        return send_from_directory(FRONTEND_DIST, 'index.html')

if __name__ == "__main__":
    print(f"🚀 FireVision Production Server Running on http://0.0.0.0:5000")
    print(f"📁 Serving Frontend from: {FRONTEND_DIST}")
    serve(app, host='0.0.0.0', port=5000, threads=6)

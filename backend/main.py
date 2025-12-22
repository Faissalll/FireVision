import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    # Use PORT from environment (Railway sets this) or default to 5000
    port = int(os.getenv('PORT', 5000))
    print(f"🚀 Starting server on port {port}")
    # Threaded=True is important for Streaming + API concurency
    # Debug should be False in production
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)

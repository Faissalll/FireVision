from app import create_app

app = create_app()

if __name__ == '__main__':
    # Threaded=True is important for Streaming + API concurency
    app.run(host='0.0.0.0', port=7860, debug=True, threaded=True)

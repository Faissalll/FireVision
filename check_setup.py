import os
import sys

print("🔍 DIAGNOSTIC START")
print(f"📂 CWD: {os.getcwd()}")

# 1. Check Imports
print("\n[1] Checking Imports...")
try:
    import cv2
    print(f"  ✅ OpenCV: {cv2.__version__}")
except ImportError as e:
    print(f"  ❌ OpenCV Missing: {e}")

try:
    import ultralytics
    print(f"  ✅ Ultralytics: {ultralytics.__version__}")
except ImportError as e:
    print(f"  ❌ Ultralytics Missing: {e}")

try:
    import flask
    from flask_cors import CORS
    print(f"  ✅ Flask: {flask.__version__}")
except ImportError as e:
    print(f"  ❌ Flask/CORS Missing: {e}")

# 2. Check Model File
print("\n[2] Checking Model File...")
model_name = "best (17).pt"
model_path = os.path.join(os.getcwd(), model_name)

if os.path.exists(model_path):
    print(f"  ✅ Model file found at: {model_path}")
    print(f"  📦 Size: {os.path.getsize(model_path) / 1024 / 1024:.2f} MB")
else:
    print(f"  ❌ Model file NOT FOUND at: {model_path}")
    # List dir
    print(f"  📂 Files in current dir: {os.listdir(os.getcwd())}")

# 3. Load Model
print("\n[3] Attempting to Load Model...")
if os.path.exists(model_path):
    try:
        from ultralytics import YOLO
        model = YOLO(model_path)
        print("  ✅ Model Loaded Successfully!")
        print(f"  🧠 Names: {model.names}")
    except Exception as e:
        print(f"  ❌ Failed to load model: {e}")
else:
    print("  ⚠️ Skipped (No file)")

print("\n🏁 DIAGNOSTIC END")

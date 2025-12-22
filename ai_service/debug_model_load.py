import os
import sys
from ultralytics import YOLO

def test_load():
    print("--- DEBUG MODEL LOAD START ---")
    
    # Current File: ai_service/debug_model_load.py
    # Root: ai_service
    base_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Base Directory (wrapper): {base_dir}")
    
    # Check current directory content
    print(f"Files in {base_dir}:")
    for f in os.listdir(base_dir):
        print(f" - {f}")

    possible_names = ['best (13).pt', 'best (17).pt', 'best.pt', 'yolov8n.pt']
    
    found_any = False
    for name in possible_names:
        model_path = os.path.join(base_dir, name)
        print(f"\nChecking Path: {model_path}")
        
        if os.path.exists(model_path):
            print(f"  [OK] File exists.")
            found_any = True
            try:
                print(f"  [..] Attempting YOLO load...")
                model = YOLO(model_path)
                print(f"  [SUCCESS] Model loaded! Classes: {model.names}")
                return # Exit on first success
            except Exception as e:
                print(f"  [FAIL] Exception during load: {e}")
                import traceback
                traceback.print_exc()
        else:
            print(f"  [MISSING] File not found.")
            
    if not found_any:
        print("\n[CRITICAL] No model files found in the directory.")
        
    print("--- DEBUG MODEL LOAD END ---")

if __name__ == "__main__":
    test_load()

import cv2

for idx in range(3):
    print(f"➤ Coba kamera index {idx}")
    cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print(f"  ❌ Kamera index {idx} tidak bisa dibuka")
        continue

    ret, frame = cap.read()
    if not ret:
        print(f"  ⚠️ Kamera index {idx} terbuka, tapi gagal baca frame")
    else:
        print(f"  ✅ Kamera index {idx} BERHASIL baca frame")
    cap.release()

import requests
import cv2

class TelegramNotifier:
    def __init__(self, token: str, chat_id: str, timeout: int = 15):
        self.token = token
        self.chat_id = chat_id
        self.api = f"https://api.telegram.org/bot{self.token}"
        self.timeout = timeout

    def send_message(self, text: str, parse_mode: str = "Markdown"):
        """
        Kirim pesan teks ke Telegram (sama seperti test_tele.py)
        """
        url = f"{self.api}/sendMessage"
        data = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": parse_mode,
        }
        r = requests.post(url, data=data, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def send_photo(self, image_bytes: bytes, caption: str | None = None):
        """
        Kirim foto (bytes) + optional caption ke Telegram.
        """
        url = f"{self.api}/sendPhoto"
        files = {"photo": ("frame.jpg", image_bytes, "image/jpeg")}
        data = {"chat_id": self.chat_id}
        if caption:
            data["caption"] = caption

        r = requests.post(url, data=data, files=files, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def send_photo_from_cv2(self, frame, caption: str | None = None, quality: int = 85):
        """
        Terima frame OpenCV (ndarray), encode ke JPG, lalu kirim.
        """
        ok, buf = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
        if not ok:
            return self.send_message(caption or "🔔 Notifikasi dari FireVision")
        return self.send_photo(buf.tobytes(), caption=caption)

    def send_notification(self, message: str, frame=None):
        """
        Wrapper: kalau ada frame, kirim foto + caption.
        Kalau tidak, kirim teks saja.
        """
        if frame is not None:
            return self.send_photo_from_cv2(frame, caption=message)
        return self.send_message(message)

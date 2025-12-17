import requests

class TelegramNotifier:
    def __init__(self, token: str, chat_id: str, timeout: int = 15):
        self.token = token
        self.chat_id = chat_id
        self.api = f"https://api.telegram.org/bot{self.token}"
        self.timeout = timeout

    def send_message(self, text: str, parse_mode: str = "Markdown"):
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
        url = f"{self.api}/sendPhoto"
        files = {"photo": ("frame.jpg", image_bytes, "image/jpeg")}
        data = {"chat_id": self.chat_id}
        if caption:
            data["caption"] = caption

        r = requests.post(url, data=data, files=files, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    # send_photo_from_cv2 REMOVED (Legacy, requires opencv-headless which is too heavy for backend)

    def send_notification(self, message: str, frame=None):
        # Frame ignored for now in minimal backend
        return self.send_message(message)

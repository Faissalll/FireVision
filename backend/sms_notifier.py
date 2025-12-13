import requests

class SMSNotifier:
    def __init__(self, api_key: str, timeout: int = 15):
        self.api_key = api_key
        self.api_url = "https://api.fonnte.com/send"
        self.timeout = timeout

    def send_sms(self, phone_number: str, message: str):
        headers = {
            "Authorization": self.api_key
        }
        
        data = {
            "target": phone_number,
            "message": message,
            "countryCode": "62"
        }
        
        try:
            response = requests.post(
                self.api_url, 
                headers=headers, 
                data=data, 
                timeout=self.timeout
            )
            result = response.json()
            
            if result.get("status"):
                print(f"✅ SMS terkirim ke {phone_number}")
                return {"success": True, "data": result}
            else:
                print(f"❌ SMS gagal: {result.get('reason', 'Unknown error')}")
                return {"success": False, "error": result.get("reason")}
                
        except Exception as e:
            print(f"❌ Error kirim SMS: {e}")
            return {"success": False, "error": str(e)}

    def send_whatsapp(self, phone_number: str, message: str):
        headers = {
            "Authorization": self.api_key
        }
        
        data = {
            "target": phone_number,
            "message": message,
            "countryCode": "62"
        }
        
        try:
            response = requests.post(
                self.api_url, 
                headers=headers, 
                data=data, 
                timeout=self.timeout
            )
            result = response.json()
            
            if result.get("status"):
                print(f"✅ WhatsApp terkirim ke {phone_number}")
                return {"success": True, "data": result}
            else:
                print(f"❌ WhatsApp gagal: {result.get('reason', 'Unknown error')}")
                return {"success": False, "error": result.get("reason")}
                
        except Exception as e:
            print(f"❌ Error kirim WhatsApp: {e}")
            return {"success": False, "error": str(e)}

    def send_fire_alert(self, phone_number: str, camera_id: str = "Main"):
        message = f"""🔥 PERINGATAN KEBAKARAN!

FireVision mendeteksi api pada:
📹 Kamera: {camera_id}
🕐 Waktu: Sekarang

Segera periksa lokasi!

- FireVision Alert System"""
        
        return self.send_whatsapp(phone_number, message)

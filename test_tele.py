import requests


TOKEN = "8092461515:AAH1mB855P5-joxZ-eZQ3dBNKmqvO9yipSc"

CHAT_ID = "1805496530"  

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
print("FULL URL:", url)   

data = {
    "chat_id": CHAT_ID,
    "text": "🔥 Test FireVision — token OK!"
}

r = requests.post(url, data=data, timeout=10)
print("STATUS:", r.status_code)
print("RESPONSE:", r.text)

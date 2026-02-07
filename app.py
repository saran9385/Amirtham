from flask import Flask, request
from flask_cors import CORS
from twilio.rest import Client
import os
from dotenv import load_dotenv 
app = Flask(__name__)
CORS(app)

# Twilio credentials
load_dotenv()  # Load variables from .env

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
FROM_WHATSAPP = os.getenv("FROM_WHATSAPP")
ADMIN_WHATSAPP = os.getenv("ADMIN_WHATSAPP")

# Twilio client
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

# Publicly accessible image URL to send
IMAGE_URL = "https://image2url.com/r2/default/images/1770401631954-0248fe4e-fd50-4394-9bf5-5551c447c330.jpg"  # <-- replace with your image

@app.route('/send_booking', methods=['POST'])
def send_booking():
    data = request.form

    # Build booking message
    message = (
        "🏨 *Amritham Holiday Home* – New Booking Alert 🏨\n\n"
        "*Guest Details:*\n"
        f"* Name:* {data.get('name')}\n"
        f"* Phone:* {data.get('phone')}\n"
        f"* Email:* {data.get('email') or 'N/A'}\n\n"
        "*Booking Details:*\n"
        f"* Check-in:* {data.get('checkin')}\n"
        f"* Check-out:* {data.get('checkout')}\n"
        f"* Room Type:* {data.get('room_type')}\n"
        f"* Special Requests:* {data.get('requests') or 'None'}\n\n"
        "📌 Please contact the guest to confirm the booking."
    )

    print("Booking message:\n", message)

    # Try sending WhatsApp message with image
    try:
        msg = client.messages.create(
            body=message,
            from_=FROM_WHATSAPP,
            to=ADMIN_WHATSAPP,
            media_url=[IMAGE_URL]  # Send the image along with the text
        )
        print("WhatsApp message SID:", msg.sid)
        status = "sent"
    except Exception as e:
        print("Error sending WhatsApp message:", e)
        status = "failed"
        msg = None

    return {
        "status": status,
        "message_sid": getattr(msg, "sid", None)
    }

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)

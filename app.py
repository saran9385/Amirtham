from flask import Flask, request, render_template
from flask_cors import CORS
from twilio.rest import Client
import os
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

# Load environment variables
load_dotenv()

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
FROM_WHATSAPP = os.getenv("FROM_WHATSAPP")
ADMIN_WHATSAPP = os.getenv("ADMIN_WHATSAPP")

client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

IMAGE_URL = "https://image2url.com/r2/default/images/1770401631954-0248fe4e-fd50-4394-9bf5-5551c447c330.jpg"

# --------------------
# PAGE ROUTES
# --------------------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/rooms")
def rooms():
    return render_template("rooms.html")

@app.route("/experience")
def dinning():
    return render_template("dinning.html")

@app.route("/gallery")
def gallery():
    return render_template("gallery.html")

@app.route("/news")
def news():
    return render_template("news.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

# @app.route("/blog")
# def blog():
#     return render_template("single-blog.html")

# --------------------
# BOOKING API
# --------------------

@app.route("/send_booking", methods=["POST"])
def send_booking():
    data = request.form

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

    try:
        msg = client.messages.create(
            body=message,
            from_=FROM_WHATSAPP,
            to=ADMIN_WHATSAPP,
            media_url=[IMAGE_URL]
        )
        return {"status": "sent", "sid": msg.sid}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)


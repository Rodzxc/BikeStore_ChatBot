from flask import Blueprint, request
from .verify import verify_fb_signature
from .limiter import load_paused_users, save_paused_users
from .admin import admin_cmd
from .handlers import response_agent, send_message
from config import load_env
import os

# ==== Conexion a Messenger ====
webhook_bp = Blueprint("webhook", __name__)

load_env()
OWNER_IDS = os.environ['OWNER_IDS']

paused_users= load_paused_users()

@webhook_bp.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == 'GET':
        verify_token = 'michatbot_token'
        if request.args.get('hub.verify_token') == verify_token:
            return request.args.get('hub.challenge')
        return 'Token inválido', 403

    if request.method == 'POST':
        if not verify_fb_signature():
            return "❌ Firma inválida", 403
        
        data = request.get_json()
        print("🔔 Mensaje recibido:")
        print(data)

        for entry in data.get("entry", []):
            for messaging_event in entry.get("messaging", []):
                sender_id = messaging_event["sender"]["id"]

                if "message" in messaging_event and "text" in messaging_event["message"]:
                    user_message = messaging_event["message"]["text"]

                    if sender_id in OWNER_IDS:
                        if admin_cmd(sender_id, user_message, paused_users, save_paused_users, send_message):
                            return "ok", 200

                    if sender_id in paused_users:
                        print(f"⏸️ Bot pausado para {sender_id}")
                        return "ok", 200

                    response_agent(sender_id, user_message)

                elif "postback" in messaging_event:
                    payload = messaging_event["postback"].get("payload", "")
                    print(f"👉 Postback recibido: {payload}")
                    if payload == "WELCOME_MESSAGE":
                        response_agent(sender_id, "¡Hola! ¿En qué puedo ayudarte?")

        return "ok", 200
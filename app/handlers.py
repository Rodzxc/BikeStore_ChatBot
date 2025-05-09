import requests, os
from agent import run_agent
from config import load_env

# ==== Cargar variable ====
load_env()
token=os.environ['PAGE_ACCESS_TOKEN']

# ==== Respuesta ====
def response_agent(recipient_id, user_message):
    print("📝 Mensaje del usuario:", user_message)
    response_text = run_agent(recipient_id, user_message)
    send_message(recipient_id, response_text)

# ==== Enviar respuesta ====
def send_message(recipient_id, message_text):
    url = f"https://graph.facebook.com/v17.0/me/messages?access_token={token}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    response = requests.post(url, headers=headers, json=payload)
    print("✅ Enviando respuesta:", response.status_code, response.text)
    print("🤖 Respuesta del agente:", message_text)
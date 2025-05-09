from flask import request
from config import load_env
import os, hmac, hashlib

# === Validar la firma del header ===
def verify_fb_signature():
    load_env()
    app_secret = os.environ["APP_SECRET"]
    signature = request.headers.get("X-Hub-Signature-256")
    if not signature:
        return False
    try:
        method, received_hash = signature.split('=')
    except ValueError:
        return False
    if method != 'sha256':
        return False
    expected_hash = hmac.new(
        app_secret.encode("utf-8"),
        msg=request.data,
        digestmod=hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(received_hash, expected_hash)
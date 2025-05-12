from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import load_env 
import os

# ==== Cargar variable ====
load_env()
if os.getenv("FLASK_ENV") != "production":
    redis_uri = os.environ["REDIS_URI"]
    rate_limiter = Limiter(
        get_remote_address,
        storage_uri=redis_uri,
        default_limits=["5 per minute"]
    )
else:
    rate_limiter = Limiter(
        get_remote_address,
        default_limits=["5 per minute"]
    )

# ==== App ====
def create_app():
    from .webhook import webhook_bp

    app = Flask(__name__)
    rate_limiter.init_app(app)

    app.register_blueprint(webhook_bp)

    return app
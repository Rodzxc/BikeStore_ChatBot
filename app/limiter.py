import os, json

# ==== Usuarios con bot pausado ====
PAUSED_USERS_FILE = "paused_users.json"

def load_paused_users():
    if os.path.exists(PAUSED_USERS_FILE):
        try:
            with open(PAUSED_USERS_FILE, "r") as f:
                return set(json.load(f))
        except:
            return set()
    return set()

def save_paused_users(paused_users):
    with open(PAUSED_USERS_FILE, "w") as f:
        json.dump(list(paused_users), f)

# ==== Pausar bot ====
def admin_cmd(sender_id, user_message, paused_users, save_paused_users, send_message):
    if user_message.startswith("/pausar "):
        target_id = user_message.split("/pausar ")[1].strip()
        paused_users.add(target_id)
        save_paused_users()
        send_message(sender_id, f"🤖⏸️ Bot pausado para usuario {target_id}")
        return True

    elif user_message.startswith("/activar "):
        target_id = user_message.split("/activar ")[1].strip()
        paused_users.discard(target_id)
        save_paused_users()
        send_message(sender_id, f"🤖▶️ Bot activado para usuario {target_id}")
        return True

    elif user_message.strip() == "/pausados":
        ids = "\n".join(paused_users) or "Ninguno"
        send_message(sender_id, f"Usuarios pausados:\n{ids}")
        return True

    return False
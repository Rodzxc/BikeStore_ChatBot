from langgraph.prebuilt import create_react_agent
from .llm import model
from .tools import tools
from .prompt import prompt_
from .memory import memory_checkpointer
from .chat_control import SupabaseChat
from config import load_env
import os, re


# ==== Cargar variables ====
load_env()
SUPABASE_URL = os.environ['SUPABASE_URL']
SUPABASE_KEY = os.environ['SUPABASE_API_KEY']

# ==== Constructor del agente ====
def build_agent(checkpointer=None, prompt=None):
    return create_react_agent(model, tools=tools, checkpointer=checkpointer, prompt=prompt)

# ==== Sanitizador de entrada ====
def sanitize_input(user_message):
    blacklist = [
        r"(ignore\s+previous\s+instructions)",
        r"(disregard\s+all\s+above)",
        r"(DROP|DELETE|INSERT|UPDATE|ALTER|TRUNCATE)\s",
        r"(prompt|shutdown|reboot|exec\s|system\()",
    ]
    for pattern in blacklist:
        if re.search(pattern, user_message, re.IGNORECASE):
            print("🚨 Mensaje potencialmente malicioso detectado")
            return False ,"[Mensaje bloqueado por razones de seguridad. Intente otra consulta]"
    return True, user_message.strip()

# ==== Correr agente ====
def run_agent(recipient_id, user_message):
# --- Sanitizar el mensaje ---
    is_valid, clean_message = sanitize_input(user_message)
    if is_valid:
# --- Armar el agente con prompt y memoria ---
        system_message= prompt_(clean_message)
        with memory_checkpointer() as checkpointer:
            agent = build_agent(checkpointer=checkpointer, prompt=system_message)
            config =  {"configurable": {"thread_id": recipient_id}}
# --- Conexion al historial de chats e ingentacion de datos ---
            supabase = SupabaseChat()
            supabase.supabase_client(SUPABASE_URL, SUPABASE_KEY)
            try:
                steps, query, response_text = supabase.extract_s_q_r(agent, config, clean_message)
            except Exception as e:
                print(f"💥 Error al ejecutar el agente: {e}")
                response_text = "¡Ocurrió un error interno! Intenta de nuevo en unos minutos."
                steps, query = "" , ""       
        try:
            supabase.insert_chat_data('Message_steps', recipient_id, clean_message, steps, query, response_text)
        except Exception as e:
            print(f"💥 Error al insertar en Supabase: {e}")
            
# --- Respuesta del agente ---
        return(response_text)
    
    else: return(clean_message)
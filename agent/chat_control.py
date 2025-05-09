from supabase import create_client, Client
import json

# ==== Historial del chat ====
class SupabaseChat:
    def __init__(self):
        self.client = None

# --- Cliente ---        
    def supabase_client(self, SUPABASE_URL:str, SUPABASE_KEY:str):
        self.client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        return self.client

# --- Insertar chat ---   
    def insert_chat_data(self, table:str, thread_id:int, user_question:str, steps:str, query:str, answer:str):
        if self.client is None:
            raise ValueError("❌ Supabase client no inicializado. Llama primero a `supabase_client()`.")
        try:
            response = (
                self.client
                .table(table)
                .insert({
                    "thread_id": thread_id,
                    "user_question": user_question,
                    "steps": steps, #s
                    "query": query, #q
                    "response": answer #r
                })
                .execute()
            )
            return response
        except Exception as e:
            print(f"Error al insertar datos en Supabase: {e}")
            return None

# --- Extraer datos --- 
    def extract_s_q_r(self, agent, config, user_message):
        titles = []
        steps = ""
        query = ""
        response_text = ""
        for step in agent.stream(
                    {"messages": [{"role": "user", "content": user_message}]},
                    stream_mode="values",
                    config=config,
                ):
                    last_msg = step["messages"][-1]
                    kwargs = last_msg.additional_kwargs
                    if kwargs :
                        for i in kwargs.values():
                            if i['name'] == 'sql_db_query':
                                query = json.loads(i['arguments'])['query']

                    role_message = last_msg.type.title()
                    name_tool = last_msg.name
                    title = (f'{role_message}({name_tool})') if name_tool != None else (f'{role_message}')
                    titles.append(title)
                    response_text = last_msg.content
                    steps = ', '.join(titles)
                    
        return  steps, query, response_text
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from config import load_env
import os
from agent.llm import model

# ==== Cargar variables ====
load_env()
uri = os.environ['RAILWAY_DDBB_URI']

# ==== BBDD de los productos ====
db = SQLDatabase.from_uri(uri,
                          view_support=True, # para ver la ventana 'availableproduct'
                          ignore_tables= ['product', 'location', 'productinventory'])

sql_db_available_products_toolkit = SQLDatabaseToolkit(db=db, llm=model)

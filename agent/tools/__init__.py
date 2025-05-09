from .database import sql_db_available_products_toolkit
from .search import proper_nouns_tool
from .translator_subcategory import translator_subcategory_es_en_tool

# ==== Lista de herramientas ====
tools = []
tools += sql_db_available_products_toolkit.get_tools()
tools.append(proper_nouns_tool)
tools.append(translator_subcategory_es_en_tool)
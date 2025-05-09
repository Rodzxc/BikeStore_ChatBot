from langchain_google_genai import ChatGoogleGenerativeAI
from config import load_env
import os

# ==== Cargar variable ====
load_env()
api_key = os.environ['GOOGLE_API_KEY']

# ==== Modelo llm ====
model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=api_key
)
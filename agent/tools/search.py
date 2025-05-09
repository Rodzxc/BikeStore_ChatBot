from langchain.agents.agent_toolkits import create_retriever_tool
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from config import load_env
import os

# ==== Modelo de embeddings ====
embeddings= HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# ==== Cargar variables ====
load_env()
pinecone_api_key = os.environ['PINECONE_APY']
pc = Pinecone(api_key=pinecone_api_key)

# ==== Conectar al indice ====
index_name = "dense-index"
index = pc.Index(index_name)
vector_store = PineconeVectorStore(embedding=embeddings, index=index)

# ==== Retriever tool Marcas y modelos ====
retriever = vector_store.as_retriever(search_kwargs={"k": 5})
description = (
    "Use to look up values to filter on. Input is an approximate spelling "
    "of the proper noun, output is valid proper nouns. Use the noun most "
    "similar to the search."
)
proper_nouns_tool = create_retriever_tool(
    retriever,
    name="search_proper_nouns",
    description=description,
)
import os
from vanna.openai import OpenAI_Chat
from src.core.azure_client import Azure_Client
# from vanna.chromadb import ChromaDB_VectorStore
from src.core.azure_custom_db import AzureAISearch_VectorStore

current_dir = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(current_dir, '..', 'db')


class MyVanna(AzureAISearch_VectorStore, OpenAI_Chat):
    def __init__(self, config=None):
        # ChromaDB_VectorStore.__init__(self, config=config)
        AzureAISearch_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, client=Azure_Client(), config=config)
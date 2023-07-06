import os

from embedchain.config.BaseConfig import BaseConfig

from embedchain.vectordb.chroma_db import ChromaDB
from chromadb.utils import embedding_functions

class InitConfig(BaseConfig):
    def __init__(self, ef=None, db=None):
        # Embedding Function
        if ef is None:
            self.ef = embedding_functions.OpenAIEmbeddingFunction(
                api_key=os.getenv("OPENAI_API_KEY"),
                organization_id=os.getenv("OPENAI_ORGANIZATION"),
                model_name="text-embedding-ada-002"
            )
        else:
            self.ef = ef

        if db is None:
            self.db = ChromaDB(ef=self.ef)
        else:
            self.db = db

        return


    def _set_embedding_function(self, ef):
        self.ef = ef
        return        

import chromadb
from chromadb.config import Settings
from typing import Optional, Dict

class ChromsDBService:
    def __init__(self):
        self.chromadb_client = chromadb.Client(Settings(
            anonymized_telemetry=False,
            allow_reset=True
        ))

    def chromadb_client(self):
        return self.chromadb_client   
    
    def get_or_create_collection(self, name: str, metadata: Optional[Dict] = None):
        return self.chromadb_client.get_or_create_collection(name, metadata=metadata)
from motor.motor_asyncio import AsyncIOMotorClient
from src.config.config import settings

class MongoDB:
    def __init__(self):
        self.client = None
        self.db = None

    async def connect(self):
        # Usamos la URL que Pydantic validó desde el entorno
        self.client = AsyncIOMotorClient(settings.mongo_url)
        self.db = self.client.pdf_database 
        print(f"Conectado a MongoDB en: {settings.mongo_url.split('@')[-1]}")

    async def close(self):
        if self.client:
            self.client.close()

db_connection = MongoDB()
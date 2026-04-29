import pytest
from motor.motor_asyncio import AsyncIOMotorClient
from src.config.config import settings

@pytest.mark.asyncio
async def test_mongodb_connection():
    # Intentamos crear el cliente usando nuestra configuración
    client = AsyncIOMotorClient(settings.mongo_url)
    
    # El comando 'ping' es la forma estándar de verificar la conexión
    response = await client.admin.command("ping")
    
    assert response["ok"] == 1.0
    client.close()

@pytest.mark.asyncio
async def test_insert_and_find_document():
    # 1. Arrange (Preparar)
    from src.database.mongodb import db_connection
    db_connection.connect()
    collection = db_connection.db.documents # Creamos/usamos una colección llamada 'documents'
    
    documento_ejemplo = {
        "filename": "test.pdf",
        "content": "Este es un texto extraído",
        "checksum": "123456789abcdef"
    }

    # 2. Act (Actuar)
    result = await collection.insert_one(documento_ejemplo)
    found_doc = await collection.find_one({"_id": result.inserted_id})

    # 3. Assert (Verificar)
    assert found_doc is not None
    assert found_doc["filename"] == "test.pdf"
    assert found_doc["checksum"] == "123456789abcdef"
    
    # Limpieza: Borramos el rastro del test
    await collection.delete_one({"_id": result.inserted_id})
    db_connection.close()
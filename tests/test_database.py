import pytest
from src.database.mongodb import db_connection

@pytest.mark.asyncio
async def test_insert_and_find_document():
    # 1. Arrange (Preparar) 
    # Iniciamos la conexión y seleccionamos la colección de resultados procesados
    await db_connection.connect()
    collection = db_connection.db.processed_pdfs
    
    # Creamos un documento con los campos reales que usará el servicio
    documento_ejemplo = {
        "filename": "documento_universidad.pdf",
        "content": "Texto extraído de prueba para validar la base de datos.",
        "checksum": "sha256_mock_789xyz"
    }

    # 2. Act (Actuar) 
    # Insertamos el documento en MongoDB
    result = await collection.insert_one(documento_ejemplo)
    # Buscamos el documento recién creado usando su ID único
    found_doc = await collection.find_one({"_id": result.inserted_id})

    # 3. Assert (Verificar) 
    # Nos aseguramos de que el documento existe y los datos coinciden
    assert found_doc is not None
    assert found_doc["filename"] == "documento_universidad.pdf"
    assert found_doc["checksum"] == "sha256_mock_789xyz"
    
    # 4. Teardown (Limpieza)
    # Borramos el rastro del test para que la base de datos local no se ensucie
    await collection.delete_one({"_id": result.inserted_id})
    await db_connection.close()
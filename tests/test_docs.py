import pytest
import io
import fitz 
from httpx import AsyncClient, ASGITransport
from src.main import app 
from src.database.mongodb import db_connection


@pytest.fixture
async def client():
    await db_connection.connect()
    await db_connection.db["processed_pdfs"].delete_many({}) 
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    
    await db_connection.close()

async def test_upload_pdf_and_verify_in_db(client: AsyncClient):
    
    doc = fitz.open() 
    page = doc.new_page() 
    text_to_test = "Este es un texto de prueba para el test de integracion."
    page.insert_text((50, 50), text_to_test)
    
  
    pdf_buffer = io.BytesIO()
    doc.save(pdf_buffer)
    file_content = pdf_buffer.getvalue() 
    doc.close()

    files = {"file": ("test_generado.pdf", file_content, "application/pdf")}
    
    response = await client.post("/documents/upload", files=files)
    
    assert response.status_code == 201
    
    db = db_connection.db
    doc_in_db = await db["processed_pdfs"].find_one({"filename": "test_generado.pdf"})
    
    assert doc_in_db is not None

    assert text_to_test in doc_in_db["content"]
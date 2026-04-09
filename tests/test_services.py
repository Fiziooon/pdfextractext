# tests/test_services.py
from src.services.pdf_processor import is_pdf, get_file_hash, extract_text, PDFProcessingError
import pytest, fitz

def test_is_pdf_valid():
    assert is_pdf("documento.pdf") is True

def test_is_pdf_invalid():
    assert is_pdf("nota.txt") is False

def test_get_file_hash_consistency():
    content = b"hola"
    # El hash SHA-256 de "hola" siempre es este:
    expected_hash = "b221d9dbb083a7f33428d7c2a3c3198ae925614d70210e28716ccaa7cd4ddb79"
    assert get_file_hash(content) == expected_hash

def test_extract_text_basic():
    # Creamos un PDF real en memoria para la prueba
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 50), "Hola mundo")
    pdf_bytes = doc.write()
    doc.close()

    # Ahora probamos la extracción con bytes de un PDF real
    result = extract_text(pdf_bytes)
    assert "Hola mundo" in result

def test_extract_text_corrupt_file():
    # Enviamos basura en lugar de un PDF
    content = b"esto no es un pdf"
    with pytest.raises(PDFProcessingError):
        extract_text(content)
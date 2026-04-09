import hashlib, fitz

class PDFProcessingError(Exception):
    """Excepción lanzada cuando falla el procesamiento del PDF"""
    pass

def is_pdf(filename: str) -> bool:
    """Verifica si la extensión es .pdf"""
    return filename.lower().endswith(".pdf")

def get_file_hash(file_content: bytes) -> str:
    """Genera un hash SHA-256 a partir de los bytes de un archivo"""
    sha256_hash = hashlib.sha256()
    sha256_hash.update(file_content)
    return sha256_hash.hexdigest()

def extract_text(file_content: bytes) -> str:
    try:
        doc = fitz.open(stream=file_content, filetype="pdf")
        full_text = ""
        for page in doc:
            full_text += page.get_text() + "\n"
        doc.close()
        return full_text
    except Exception as e:
        # En lugar de dejar que el programa falle, lanzamos nuestro error
        raise PDFProcessingError(f"No se pudo procesar el PDF: {str(e)}")
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from src.database.mongodb import db_connection
from src.services.pdf_service import extract_text_from_pdf, get_pdf_checksum
from src.models.document import DocumentCreate

router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="El archivo debe ser un PDF")

    pdf_bytes = await file.read()
    if len(pdf_bytes) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="El archivo es demasiado grande")

    checksum = get_pdf_checksum(pdf_bytes)
    
    db = db_connection.db
    existing_doc = await db["processed_pdfs"].find_one({"checksum": checksum})
    if existing_doc:
        raise HTTPException(status_code=400, detail="El documento ya ha sido procesado anteriormente")

    text_content = extract_text_from_pdf(pdf_bytes)


    new_doc = DocumentCreate(
        filename=file.filename,
        content=text_content,
        checksum=checksum,
        size_bytes=len(pdf_bytes)
    )

    await db["processed_pdfs"].insert_one(new_doc.model_dump())

    return {"message": "PDF procesado exitosamente", "filename": file.filename}
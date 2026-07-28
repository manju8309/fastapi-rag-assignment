from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Document, DocumentChunk
from app.rag import chunk_text, create_embedding

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


@router.post("/ingest")
async def ingest_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    if not file.filename.endswith(".txt"):
        raise HTTPException(
            status_code=400,
            detail="Only .txt files are supported"
        )

    content = await file.read()
    text = content.decode("utf-8")

    document = Document(
        filename=file.filename,
        content=text,
        user_id=1
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    chunks = chunk_text(text)

    for chunk in chunks:

        embedding = create_embedding(chunk)

        db_chunk = DocumentChunk(
            document_id=document.id,
            chunk_text=chunk,
            embedding=str(embedding)
        )

        db.add(db_chunk)

    db.commit()

    return {
        "message": "Document ingested successfully",
        "document_id": document.id,
        "chunks_created": len(chunks)
    }
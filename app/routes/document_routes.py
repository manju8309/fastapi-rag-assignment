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
    # Check file type
    if not file.filename or not file.filename.lower().endswith(".txt"):
        raise HTTPException(
            status_code=400,
            detail="Only .txt files are supported"
        )

    try:
        # Read uploaded file
        content = await file.read()

        # Convert bytes to text
        text = content.decode("utf-8")

        # Check if file is empty
        if not text.strip():
            raise HTTPException(
                status_code=400,
                detail="The uploaded file is empty"
            )

        # Save document
        document = Document(
            filename=file.filename,
            content=text,
            user_id=1
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        # Split document into chunks
        chunks = chunk_text(text)

        # Generate embedding for each chunk
        for chunk in chunks:

            embedding = create_embedding(chunk)

            db_chunk = DocumentChunk(
                document_id=document.id,
                chunk_text=chunk,
                embedding=str(embedding)
            )

            db.add(db_chunk)

        # Save all chunks
        db.commit()

        return {
            "message": "Document ingested successfully",
            "document_id": document.id,
            "filename": file.filename,
            "chunks_created": len(chunks)
        }

    except UnicodeDecodeError:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail="The file must be a valid UTF-8 text file"
        )

    except HTTPException:
        db.rollback()
        raise

    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Document ingestion failed: {str(e)}"
        )
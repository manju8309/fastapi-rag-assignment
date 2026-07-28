from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import DocumentChunk
from app.rag import create_embedding, cosine_similarity

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/")
def chat(
    question: str,
    db: Session = Depends(get_db)
):

    question_embedding = create_embedding(question)

    chunks = db.query(DocumentChunk).all()

    if not chunks:
        return {
            "answer": "No documents have been uploaded yet."
        }

    best_chunk = None
    best_score = -1

    for chunk in chunks:

        stored_embedding = eval(chunk.embedding)

        score = cosine_similarity(
            question_embedding,
            stored_embedding
        )

        if score > best_score:
            best_score = score
            best_chunk = chunk

    return {
        "question": question,
        "answer": best_chunk.chunk_text,
        "similarity_score": float(best_score)
    }
import ast

from fastapi import (
    APIRouter,
    Depends
)
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import (
    User,
    Document,
    DocumentChunk
)
from app.auth import get_current_user
from app.rag import (
    create_embedding,
    cosine_similarity,
    generate_answer
)


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/")
def chat(
    question: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Create embedding for the user's question
    question_embedding = create_embedding(question)

    # Get documents belonging to the authenticated user
    user_documents = db.query(Document).filter(
        Document.user_id == current_user.id
    ).all()

    if not user_documents:
        return {
            "question": question,
            "answer": "No documents have been uploaded yet.",
            "similarity_score": 0.0
        }

    # Get document IDs belonging to the current user
    document_ids = [
        document.id
        for document in user_documents
    ]

    # Get chunks belonging to the user's documents
    chunks = db.query(DocumentChunk).filter(
        DocumentChunk.document_id.in_(document_ids)
    ).all()

    if not chunks:
        return {
            "question": question,
            "answer": "No document content is available for answering the question.",
            "similarity_score": 0.0
        }

    # Find the most relevant chunks
    scored_chunks = []

    for chunk in chunks:

        if not chunk.embedding:
            continue

        try:
            # Safely convert stored string back to a Python list
            stored_embedding = ast.literal_eval(
                chunk.embedding
            )

            score = cosine_similarity(
                question_embedding,
                stored_embedding
            )

            scored_chunks.append(
                (chunk, score)
            )

        except (ValueError, SyntaxError):
            continue

    if not scored_chunks:
        return {
            "question": question,
            "answer": "Unable to retrieve relevant document content.",
            "similarity_score": 0.0
        }

    # Sort chunks by similarity score
    scored_chunks.sort(
        key=lambda x: x[1],
        reverse=True
    )

    # Select top 3 relevant chunks
    top_chunks = scored_chunks[:3]

    # Create context from the retrieved chunks
    context = "\n\n".join(
        chunk.chunk_text
        for chunk, score in top_chunks
    )

    # Get the highest similarity score
    best_score = top_chunks[0][1]

    # Generate final answer using the LLM
    answer = generate_answer(
        question,
        context
    )

    return {
        "question": question,
        "answer": answer,
        "similarity_score": float(best_score),
        "chunks_used": len(top_chunks),
        "user_id": current_user.id
    }
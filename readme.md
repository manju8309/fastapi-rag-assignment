# FastAPI RAG Assignment

## Project Overview

This project is a Retrieval-Augmented Generation (RAG) backend application built using FastAPI and PostgreSQL.

The application provides user authentication, document ingestion, text chunking, embedding generation, and retrieval of relevant document content based on user questions.

## Technologies Used

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT Authentication
- Passlib
- Sentence Transformers
- NumPy
- Uvicorn

## Features

- User signup
- User login
- Password hashing
- JWT authentication
- PostgreSQL database
- Document ingestion
- Text chunking
- Text embeddings
- Similarity-based document retrieval
- RAG chat endpoint
- Error logging middleware
- Swagger API documentation

## Project Structure

```text
app/
├── routes/
│   ├── auth_routes.py
│   ├── document_routes.py
│   └── chat_routes.py
├── auth.py
├── database.py
├── main.py
├── middleware.py
├── models.py
├── rag.py
└── schemas.py
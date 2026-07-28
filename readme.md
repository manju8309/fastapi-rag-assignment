# FastAPI + AI RAG Assignment

## Project Overview

This project is a backend application built using FastAPI that demonstrates JWT authentication, PostgreSQL database integration, document ingestion, text chunking, embeddings, semantic retrieval, and Retrieval-Augmented Generation (RAG).

The application allows users to:

- Create an account using signup.
- Login securely using JWT authentication.
- Upload and ingest text documents.
- Store documents and document chunks in PostgreSQL.
- Generate embeddings for document chunks.
- Retrieve relevant document content based on user questions.
- Use an LLM to generate answers based on the retrieved content.
- Log unhandled application errors into the database.

The project follows a modular structure to keep authentication, database, document ingestion, RAG, routes, and middleware organized separately.

---

## Features

### 1. JWT Authentication

- User signup endpoint.
- User login endpoint.
- Passwords are securely hashed using bcrypt.
- JWT access tokens are generated after successful login.
- Protected functionality can use JWT authentication.

### 2. PostgreSQL Database

PostgreSQL is used as the primary database.

The application stores:

- Users
- Documents
- Document chunks
- Embeddings
- Error logs

SQLAlchemy is used for database interaction.

### 3. Document Ingestion

The document ingestion endpoint allows users to upload text documents.

The ingestion process includes:

1. Uploading the document.
2. Storing the document.
3. Splitting the document into smaller chunks.
4. Generating embeddings for the chunks.
5. Storing the chunks and embeddings.

### 4. Retrieval-Augmented Generation (RAG)

The chat endpoint implements a basic RAG pipeline.

The process is:

1. User submits a question.
2. The question is converted into an embedding.
3. Relevant document chunks are retrieved.
4. Retrieved context is provided to the LLM.
5. The LLM generates an answer based on the relevant context.

### 5. Error Logging Middleware

Custom FastAPI middleware handles unhandled exceptions.

The middleware records information such as:

- Timestamp
- API endpoint
- HTTP method
- Error message
- Stack trace
- Authenticated user ID, when available

The error information is stored in the PostgreSQL database.

### 6. Modular Project Structure

The project is organized into separate modules for better maintainability.

---

## Technologies Used

- Python
- FastAPI
- Uvicorn
- PostgreSQL
- SQLAlchemy
- Pydantic
- JWT
- python-jose
- Passlib
- bcrypt
- Sentence Transformers
- NumPy
- OpenAI API
- python-dotenv

---

## Project Structure

```text
fastapi-rag-assignment/
│
├── app/
│   ├── __init__.py
│   ├── auth.py
│   ├── database.py
│   ├── main.py
│   ├── middleware.py
│   ├── models.py
│   ├── rag.py
│   ├── schemas.py
│   │
│   └── routes/
│       ├── __init__.py
│       ├── auth_routes.py
│       ├── chat_routes.py
│       └── document_routes.py
│
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt

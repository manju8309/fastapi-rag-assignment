# FastAPI + AI RAG Assignment

## 1. Project Overview

This project is a backend application built using FastAPI that demonstrates JWT authentication, PostgreSQL database integration, document ingestion, text chunking, embeddings, semantic retrieval, and Retrieval-Augmented Generation (RAG). The application allows users to create an account using signup, login securely using JWT authentication, upload and ingest text documents, store documents and document chunks in PostgreSQL, generate embeddings for document chunks, retrieve relevant document content based on user questions, generate answers based on retrieved document content, and log unhandled application errors into the database. The project follows a modular structure to keep authentication, database, document ingestion, RAG, routes, and middleware organized separately.

## 2. Prerequisites

Before running this project, make sure Python 3.11 or later, PostgreSQL, and Git are installed on your system. An OpenAI API key is also required for the RAG functionality. You should have a PostgreSQL database named `rag_assignment_db` and PostgreSQL should be running on the default port `5432`. Create a `.env` file in the root directory of the project and add the required environment variables such as the PostgreSQL database URL, secret key, and OpenAI API key.

Example environment configuration:

DATABASE_URL=postgresql://postgres:your_password@localhost:5432/rag_assignment_db

SECRET_KEY=your_secret_key

OPENAI_API_KEY=your_openai_api_key

Replace the placeholder values with your actual configuration. Do not upload the actual `.env` file, database passwords, or API keys to GitHub. The `.env` file is excluded from GitHub using `.gitignore`, while `.env.example` contains only placeholder values.

## 3. Steps to Install Dependencies

First, clone the repository using the following command:

git clone https://github.com/manju8309/fastapi-rag-assignment.git

Open the project directory using:

cd fastapi-rag-assignment

Create a Python virtual environment using:

python -m venv venv

Activate the virtual environment. On Windows PowerShell, use:

.\venv\Scripts\Activate.ps1

On Windows Command Prompt, use:

venv\Scripts\activate

After activating the virtual environment, install all required dependencies using:

pip install -r requirements.txt

After installing the dependencies, create a `.env` file in the root directory and configure the PostgreSQL database URL, secret key, and OpenAI API key. Use `.env.example` as a reference for the required environment variables.

## 4. Instructions to Run the Project

Before running the application, make sure the Python virtual environment is activated, PostgreSQL is running, and the `.env` file is properly configured. Start the FastAPI application using the following command:

python -m uvicorn app.main:app --reload

The application will run at `http://127.0.0.1:8000`. FastAPI provides interactive Swagger API documentation that can be accessed by opening `http://127.0.0.1:8000/docs` in a web browser. The Swagger UI can be used to test the available API endpoints.

The available API endpoints include `GET /` to check whether the API is running, `POST /auth/signup` to create a new user account, `POST /auth/login` to authenticate a user and receive a JWT token, `POST /documents/ingest` to upload and process a document, and `POST /chat/` to ask questions based on the uploaded document.

The recommended testing order is to first create a user using `/auth/signup`, then login using `/auth/login`, upload a document using `/documents/ingest`, and finally ask a question using `/chat/`. The response can then be verified to ensure that it is based on the uploaded document content.

## 5. Additional Information and Notes

The application follows a basic Retrieval-Augmented Generation (RAG) pipeline. The process starts when a user uploads a document. The document is stored in the database and split into smaller chunks. Embeddings are generated for the document chunks and stored for retrieval. When a user asks a question, the question is processed and relevant document chunks are retrieved. The relevant context is then provided to the language model to generate an answer based on the uploaded document.

The application uses PostgreSQL with SQLAlchemy for database management. The main database tables include Users, Documents, Document Chunks, and Error Logs. The Users table stores registered user information, the Documents table stores uploaded documents, the Document Chunks table stores the smaller sections created from documents along with their embeddings, and the Error Logs table stores application error information.

The application implements authentication using JWT and securely hashes user passwords using bcrypt. JWT tokens are used for authentication, and sensitive configuration values are stored in the `.env` file. The `.env` file is excluded from GitHub using `.gitignore`, and the `.env.example` file contains only placeholder values. Real database passwords and API keys should never be uploaded to GitHub.

The application also includes error logging middleware for handling unhandled application errors. The middleware can record information such as the timestamp, API endpoint, HTTP method, error message, stack trace, and user ID when available. This information is stored in the database for error tracking and debugging purposes.

The project is organized into separate modules for better maintainability. The project structure includes the `app` directory containing `auth.py` for authentication and password handling, `database.py` for database configuration, `main.py` for the FastAPI application, `middleware.py` for error handling, `models.py` for database models, `rag.py` for RAG functionality, and `schemas.py` for request and response schemas. The `routes` directory contains `auth_routes.py` for authentication endpoints, `chat_routes.py` for chat functionality, `document_routes.py` for document ingestion, and `__init__.py`.

The main technologies used in this project are Python, FastAPI, Uvicorn, PostgreSQL, SQLAlchemy, Pydantic, JWT, python-jose, Passlib, bcrypt, Sentence Transformers, NumPy, OpenAI API, and python-dotenv.

The project is developed as part of a backend assignment to demonstrate FastAPI development practices, authentication, database integration, document processing, and a basic Retrieval-Augmented Generation (RAG) pipeline. The application is intended for development and demonstration purposes.

## Project Structure

fastapi-rag-assignment/

├── app/

│   ├── __init__.py

│   ├── auth.py

│   ├── database.py

│   ├── main.py

│   ├── middleware.py

│   ├── models.py

│   ├── rag.py

│   ├── schemas.py

│   └── routes/

│       ├── __init__.py

│       ├── auth_routes.py

│       ├── chat_routes.py

│       └── document_routes.py

├── .env.example

├── .gitignore

├── README.md

└── requirements.txt

## Author

Pesala Manjusha

GitHub Repository:

https://github.com/manju8309/fastapi-rag-assignment

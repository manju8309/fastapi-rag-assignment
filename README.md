# FastAPI + AI RAG Assignment

## 1. Project Overview

This project is a backend application built using **FastAPI** that demonstrates secure authentication, PostgreSQL database integration, document ingestion, text chunking, embeddings, semantic retrieval, and a basic **Retrieval-Augmented Generation (RAG)** pipeline.

The application provides the following functionality:

* User registration through a signup endpoint
* Secure user login using JWT authentication
* Password hashing using bcrypt
* PostgreSQL database integration using SQLAlchemy
* Text document ingestion and storage
* Document chunking for efficient retrieval
* Embedding generation for document chunks
* Semantic similarity-based document retrieval
* RAG-based question answering using retrieved document content
* Custom middleware for handling unhandled application exceptions
* Error logging to the PostgreSQL database
* Modular project structure for better maintainability

The RAG pipeline allows users to upload text documents and ask questions based on the uploaded content. The system processes the document, divides it into smaller chunks, generates embeddings, retrieves relevant content based on the user's question, and uses the retrieved context to generate a relevant answer.

---

## 2. Prerequisites

Before running this project, make sure the following software and services are installed:

* Python 3.11 or later
* PostgreSQL
* Git
* An OpenAI API key

PostgreSQL should be running on the default port `5432`.

Create a PostgreSQL database named:

```text
rag_assignment_db
```

Create a `.env` file in the root directory of the project and configure the required environment variables.

Example:

```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/rag_assignment_db
SECRET_KEY=your_secret_key
OPENAI_API_KEY=your_openai_api_key
```

Replace the placeholder values with your actual configuration.

**Important:** Do not upload your actual `.env` file, database passwords, secret keys, or API keys to GitHub. The `.env` file is excluded using `.gitignore`, while `.env.example` contains only placeholder values.

---

## 3. Steps to Install Dependencies

### Step 1: Clone the Repository

```bash
git clone https://github.com/manju8309/fastapi-rag-assignment.git
```

### Step 2: Navigate to the Project Directory

```bash
cd fastapi-rag-assignment
```

### Step 3: Create a Python Virtual Environment

```bash
python -m venv venv
```

### Step 4: Activate the Virtual Environment

On Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

On Windows Command Prompt:

```cmd
venv\Scripts\activate
```

### Step 5: Install Dependencies

After activating the virtual environment, install the required packages:

```bash
pip install -r requirements.txt
```

### Step 6: Configure Environment Variables

Create a `.env` file in the root directory and configure the PostgreSQL database URL, secret key, and OpenAI API key.

Use `.env.example` as a reference for the required environment variables.

---

## 4. Instructions to Run the Project

Before running the application, make sure:

* The Python virtual environment is activated.
* PostgreSQL is running.
* The PostgreSQL database is configured correctly.
* The `.env` file contains the required environment variables.
* All dependencies are installed.

Start the FastAPI application using:

```bash
python -m uvicorn app.main:app --reload
```

The application will run locally at:

```text
http://127.0.0.1:8000
```

### API Documentation

FastAPI provides interactive Swagger API documentation at:

```text
http://127.0.0.1:8000/docs
```

The Swagger UI can be used to view and test the available API endpoints.

### Main API Endpoints

| Method | Endpoint            | Description                                                              |
| ------ | ------------------- | ------------------------------------------------------------------------ |
| GET    | `/`                 | Checks whether the API is running                                        |
| POST   | `/auth/signup`      | Creates a new user account                                               |
| POST   | `/auth/login`       | Authenticates a user and returns a JWT token                             |
| POST   | `/documents/ingest` | Uploads and processes a text document                                    |
| POST   | `/chat/`            | Accepts a question and retrieves relevant document content for answering |

### Recommended Testing Flow

1. Create a user using `/auth/signup`.
2. Login using `/auth/login`.
3. Obtain the JWT access token.
4. Upload a text document using `/documents/ingest`.
5. Ask a question using `/chat/`.
6. Verify that the response is based on the relevant uploaded document content.

---

## 5. Database and Schema Design

The application uses **PostgreSQL** as the primary database and **SQLAlchemy ORM** for database operations.

The main database tables are:

### Users

Stores registered user information, including usernames, email addresses, and securely hashed passwords.

### Documents

Stores uploaded text documents and associates them with users.

### Document Chunks

Stores smaller chunks created from uploaded documents along with their generated embeddings. These chunks are used during semantic retrieval.

### Error Logs

Stores information about unhandled application errors for monitoring and debugging purposes.

---

## 6. Database Indexing

The application uses indexes on frequently queried fields to improve database lookup performance.

The following indexes are used:

* `users.id` – Primary key index for efficient user identification.
* `users.username` – Indexed to improve username lookup during authentication.
* `users.email` – Indexed to improve email lookup and existing-user checks.
* `documents.id` – Primary key index for efficient document identification.
* `documents.user_id` – Indexed to efficiently retrieve documents associated with a specific user.
* `document_chunks.id` – Primary key index for efficient chunk identification.
* `document_chunks.document_id` – Indexed to efficiently retrieve chunks associated with a specific document.
* `error_logs.id` – Primary key index for efficient error log identification.
* `error_logs.user_id` – Indexed to efficiently retrieve error logs associated with a specific user.

These indexes were selected based on common application query patterns, particularly authentication, document ownership, document chunk retrieval, and error log retrieval.

---

## 7. Retrieval-Augmented Generation (RAG) Pipeline

The application implements a basic Retrieval-Augmented Generation pipeline.

The process works as follows:

```text
User uploads a text document
        ↓
Document is stored in PostgreSQL
        ↓
Document is split into smaller chunks
        ↓
Embeddings are generated for document chunks
        ↓
Chunks and embeddings are stored
        ↓
User submits a question
        ↓
Question embedding is generated
        ↓
Relevant document chunks are retrieved
        ↓
Retrieved context is provided to the language model
        ↓
LLM generates an answer based on the retrieved context
```

This approach allows the application to provide answers based on information contained in the uploaded documents.

---

## 8. Authentication and Security

The application implements JWT-based authentication for secure user authentication.

The authentication process includes:

* User signup
* Secure password hashing using bcrypt
* User login
* JWT token generation
* JWT-based authentication for protected operations

Sensitive configuration values, including database credentials, secret keys, and API keys, are stored in environment variables.

The `.env` file is excluded from GitHub using `.gitignore`, while `.env.example` provides placeholder values for required configuration.

Real passwords, secret keys, and API keys should never be committed to the repository.

---

## 9. Error Handling and Middleware

The application includes custom FastAPI middleware for handling unhandled application exceptions.

When an unhandled exception occurs, the middleware records relevant information such as:

* Timestamp
* API endpoint
* HTTP method
* Error message
* Stack trace
* Authenticated user ID, when available

The error information is stored in the PostgreSQL database through the `ErrorLog` table to support debugging and application monitoring.

The API also returns a JSON error response when an unhandled server-side exception occurs.

---

## 10. Project Structure

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
```

The project follows a modular structure to keep authentication, database configuration, database models, RAG functionality, API routes, and middleware organized separately.

---

## 11. Technologies Used

* Python 3.11+
* FastAPI
* Uvicorn
* PostgreSQL
* SQLAlchemy
* Pydantic
* JWT
* python-jose
* Passlib
* bcrypt
* OpenAI API
* Sentence Transformers
* NumPy
* python-dotenv

---

## 12. Deployment

The FastAPI backend is deployed on **Render** with PostgreSQL as the primary database.

The application uses environment variables for sensitive configuration such as:

* PostgreSQL database URL
* JWT secret key
* OpenAI API key

The `master` branch is used as the deployment branch for the Render service.

---

## 13. Additional Information and Notes

* This project was developed as part of a backend assignment to demonstrate FastAPI development practices, JWT authentication, database integration, document processing, and a basic RAG pipeline.
* PostgreSQL is used as the primary database.
* SQLAlchemy is used as the ORM for database operations.
* OpenAI APIs are used for embedding generation and LLM-based response generation.
* The `.env.example` file provides a template for required environment variables.
* The actual `.env` file must not be committed to GitHub.
* API keys, passwords, and other sensitive credentials must be kept private.
* The application is intended for development, demonstration, and assignment evaluation purposes.

---

## Live Deployment

- **Live API:** https://fastapi-rag-assignment.onrender.com
- **Swagger API Documentation:** https://fastapi-rag-assignment.onrender.com/docs
- **GitHub Repository:** https://github.com/manju8309/fastapi-rag-assignment

The application is deployed on Render. The Swagger API documentation can be used to test the available FastAPI endpoints.

## Author

**Pesala Manjusha**

### GitHub Repository

https://github.com/manju8309/fastapi-rag-assignment

```
```

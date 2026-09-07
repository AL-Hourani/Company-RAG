# Company RAG

A production-oriented, multi-tenant Retrieval-Augmented Generation (RAG) system designed for enterprise internal knowledge bases.

The project is being built from the ground up with a focus on **software architecture, reliability, scalability, observability, and distributed systems**, rather than simply building a basic LLM chatbot.

> **Status:** 🚧 Under active development

---

## Overview

Company RAG allows organizations to ingest internal documents, transform them into searchable chunks, generate vector embeddings, retrieve relevant knowledge, and eventually generate grounded answers using Large Language Models.

The system is designed around a multi-tenant architecture where each organization's data is logically isolated.

The long-term architecture includes:

* Document ingestion
* Document normalization
* Intelligent chunking
* Document versioning
* Content hashing
* Idempotent indexing
* Vector search
* Metadata filtering
* Hybrid retrieval
* Reranking
* Context construction
* Grounded LLM generation
* Citations
* Retrieval evaluation
* Answer evaluation
* Authentication and authorization
* Multi-tenancy
* Background processing
* Message queues
* Workers
* Retry mechanisms
* Dead-letter queues
* Observability
* Caching
* Dockerized deployment
* Production infrastructure

---

# Architecture

The project is intentionally being developed in layers.

The current high-level architecture is:

```text
                         ┌──────────────────────┐
                         │      Client/API      │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      FastAPI         │
                         │      API Layer       │
                         └──────────┬───────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
          ┌──────────────────┐            ┌──────────────────┐
          │ Ingestion        │            │ Retrieval        │
          │ Pipeline         │            │ Pipeline         │
          └────────┬─────────┘            └────────┬─────────┘
                   │                               │
                   ▼                               ▼
          ┌──────────────────┐            ┌──────────────────┐
          │ Document         │            │ Vector Search    │
          │ Processing       │            │ + Reranking      │
          └────────┬─────────┘            └────────┬─────────┘
                   │                               │
                   ▼                               ▼
          ┌──────────────────┐            ┌──────────────────┐
          │ Embeddings       │            │ Context Builder  │
          └────────┬─────────┘            └────────┬─────────┘
                   │                               │
                   ▼                               ▼
          ┌──────────────────┐            ┌──────────────────┐
          │ Vector Database  │            │ LLM Generation  │
          └──────────────────┘            └──────────────────┘

                    ┌──────────────────────────────┐
                    │          PostgreSQL          │
                    │                              │
                    │ Documents                    │
                    │ Versions                     │
                    │ Users / Tenants (future)     │
                    │ Jobs (future)                │
                    └──────────────────────────────┘
```

---

# Technology Stack

## Backend

* Python
* FastAPI
* Pydantic
* SQLAlchemy
* Alembic

## AI / RAG

* LangChain
* Google Gemini
* Gemini Embeddings
* Retrieval-Augmented Generation
* Vector Search
* Reranking

## Databases

* PostgreSQL
* Chroma

## Distributed Systems

Planned:

* RabbitMQ
* Background workers
* Retry mechanisms
* Dead-letter queues

## Infrastructure

Planned:

* Docker
* Redis
* Object Storage
* Production deployment

---

# Project Structure

The project currently follows a modular architecture:

```text
company-rag/
│
├── app/
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── session.py
│   │   └── models/
│   │       ├── __init__.py
│   │       └── document.py
│   │
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── loaders.py
│   │   ├── chunker.py
│   │   ├── identity.py
│   │   ├── models.py
│   │   ├── registry.py
│   │   └── service.py
│   │
│   ├── indexing/
│   │   ├── __init__.py
│   │   ├── embeddings.py
│   │   └── vector_store.py
│   │
│   ├── retrieval/
│   │   └── __init__.py
│   │
│   ├── generation/
│   │   └── __init__.py
│   │
│   ├── evaluation/
│   │   └── __init__.py
│   │
│   └── main.py
│
├── data/
│   └── documents/
│       ├── hr/
│       └── security/
│
├── migrations/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── tests/
│
├── scripts/
│
├── .env
├── .env.example
├── .gitignore
├── alembic.ini
├── requirements.txt
└── README.md
```

The structure will evolve as the system becomes more complex.

---

# Current Features

## Document Ingestion

The system currently supports loading text documents and attaching structured metadata.

Example metadata:

```text
tenant_id
filename
source
content_type
department
document_type
version
checksum
document_id
chunk_index
chunk_id
```

---

## Document Chunking

Documents are split using a recursive character-based text splitter.

Current configuration:

```text
chunk_size    = 800
chunk_overlap = 100
```

The chunking strategy is intentionally isolated from the rest of the ingestion pipeline so that it can later be improved and evaluated independently.

---

## Content Identity

The system calculates a SHA-256 checksum for each document.

Example:

```text
File
 │
 ▼
SHA-256
 │
 ▼
Content Identity
```

This allows the system to detect whether the document content has changed.

---

## Stable Chunk Identity

Each chunk receives a deterministic identifier.

Example:

```text
document_id:chunk:0
document_id:chunk:1
document_id:chunk:2
```

This is important for idempotent indexing and future update/delete operations.

---

## Vector Embeddings

The current embedding provider uses Google's Gemini embedding model.

Current model:

```text
gemini-embedding-001
```

The current environment produces:

```text
3072-dimensional vectors
```

The embedding provider is abstracted behind:

```text
app/indexing/embeddings.py
```

This allows the embedding implementation to be replaced later without rewriting the entire RAG architecture.

---

## Vector Database

Chroma is currently used as the vector store.

The vector store abstraction is located at:

```text
app/indexing/vector_store.py
```

Current capabilities include:

```text
Similarity Search
Similarity Search + Scores
Metadata Filtering
Tenant Filtering
```

---

# Multi-Tenancy

Multi-tenancy is treated as a **security boundary**, not simply a metadata field.

Every document contains:

```text
tenant_id
```

Retrieval can be restricted using:

```python
tenant_id="acme"
```

Conceptually:

```text
Tenant A
 ├── document 1
 ├── document 2
 └── document 3

Tenant B
 ├── document 4
 ├── document 5
 └── document 6
```

A query belonging to Tenant A must never retrieve information belonging to Tenant B.

In the final production system, the tenant identity will come from the authenticated user/session rather than being trusted from arbitrary client input.

---

# Document Lifecycle

The project uses explicit document states:

```text
NEW
 │
 ▼
PROCESSING
 │
 ├──────────────► FAILED
 │
 ▼
INDEXED
```

The purpose of the lifecycle is to make document ingestion observable and recoverable.

The system is moving from an in-memory registry toward PostgreSQL-backed document lifecycle management.

---

# Document Versioning

Documents are treated as logical entities with immutable content versions.

Example:

```text
Document
│
├── Version 1
│   └── checksum = AAA
│
├── Version 2
│   └── checksum = BBB
│
└── Version 3
    └── checksum = CCC
```

This allows the system to support:

* Document history
* Auditing
* Rollbacks
* Debugging
* Re-indexing
* Change tracking

---

# Idempotent Indexing

One of the main engineering goals is to make ingestion idempotent.

Running the same ingestion operation multiple times should not unnecessarily create duplicate vectors or embeddings.

Conceptually:

```text
Incoming File
      │
      ▼
Calculate Checksum
      │
      ▼
Find Logical Document
      │
      ├── Not Found
      │      │
      │      ▼
      │     INDEX
      │
      ├── Same Checksum
      │      │
      │      ▼
      │     SKIP
      │
      └── Different Checksum
             │
             ▼
         NEW VERSION
```

This becomes especially important once ingestion is moved to background workers.

---

# Retrieval Pipeline

The retrieval system will eventually evolve toward:

```text
User Query
    │
    ▼
Query Processing
    │
    ▼
Metadata Filtering
    │
    ▼
Vector Search
    │
    ▼
Top-K Candidates
    │
    ▼
Reranker
    │
    ▼
Top-N Relevant Chunks
    │
    ▼
Context Builder
    │
    ▼
LLM
```

The project intentionally separates retrieval from generation.

This makes it possible to determine whether a failure is caused by:

```text
Retrieval
```

or:

```text
Generation
```

instead of hiding both problems inside a single RAG chain.

---

# Evaluation

Evaluation will be treated as a first-class part of the system.

Planned metrics include:

### Retrieval

* Recall@K
* Precision@K
* MRR
* Hit Rate

### Generation

* Faithfulness
* Groundedness
* Answer relevance
* Citation correctness

The project will eventually contain a golden evaluation dataset containing:

```text
Question
Expected Documents
Expected Chunks
Expected Answer
```

---

# Production Architecture Roadmap

The project is intentionally developed through a finite sequence of phases.

## Phase 1 — Foundation

* Project architecture
* Configuration
* Environment management
* Logging
* Application structure

## Phase 2 — Ingestion

* Document loaders
* Normalization
* Metadata
* Chunking
* Chunk evaluation

## Phase 3 — Indexing

* Embeddings
* Vector database
* Collection/index design
* Stable IDs
* Idempotent indexing
* Document versioning

## Phase 4 — Retrieval

* Similarity search
* Metadata filtering
* Top-K
* MMR
* Hybrid retrieval
* Reranking

## Phase 5 — Generation

* Prompt design
* Context construction
* Grounded generation
* Citations
* Hallucination control

## Phase 6 — Evaluation

* Golden dataset
* Retrieval evaluation
* Generation evaluation
* RAG evaluation

## Phase 7 — Production API

* FastAPI
* Async architecture
* Authentication
* Authorization
* Multi-tenancy
* Rate limiting
* Caching
* Observability
* Error handling

## Phase 8 — Distributed RAG

* Background ingestion
* RabbitMQ
* Workers
* Retry mechanisms
* Dead-letter queues
* Job state management
* Horizontal scaling

## Phase 9 — Production Infrastructure

* Docker
* PostgreSQL
* Redis
* Vector database
* Object storage
* Deployment
* Monitoring
* Production hardening

---

# Development Principles

This project follows several architectural principles.

## 1. Separation of Concerns

Each responsibility should have its own component.

For example:

```text
Loader
   ↓
Chunker
   ↓
Embedding Provider
   ↓
Vector Store
   ↓
Retriever
   ↓
Generator
```

A single class should not own the entire RAG pipeline.

---

## 2. Frameworks Are Implementation Details

LangChain is used to accelerate implementation.

The architecture itself does not depend conceptually on LangChain.

For example:

```text
EmbeddingProvider
```

is an architectural abstraction.

Gemini is one implementation.

Likewise:

```text
VectorStore
```

is an architectural concept.

Chroma is one implementation.

This allows the infrastructure to evolve without rewriting the application architecture.

---

## 3. PostgreSQL Is the Source of Truth for Business State

PostgreSQL is responsible for information such as:

```text
Documents
Document Versions
Statuses
Users
Tenants
Jobs
Audit Information
```

The vector database is responsible primarily for:

```text
Embeddings
Vector Search
Retrieval Metadata
```

The vector database should not become the authoritative source for application business state.

---

## 4. Retrieval Before Generation

The system will validate retrieval independently before introducing complex generation logic.

The reasoning is simple:

```text
Bad Retrieval
     ↓
Bad Context
     ↓
Bad Answer
```

An LLM cannot reliably generate a correct answer if the relevant information was never retrieved.

---

## 5. Design for Failure

Production systems must assume failures will happen.

Examples:

```text
Network failure
Database failure
Embedding API failure
Vector DB failure
Worker crash
Process restart
Duplicate message
Timeout
Partial indexing
```

The architecture will therefore progressively introduce:

```text
Retries
Idempotency
Timeouts
Dead-letter queues
State tracking
Observability
Recovery
```

---

# Local Development

## 1. Clone the Repository

```bash
git clone <repository-url>
cd company-rag
```

## 2. Create Virtual Environment

Windows PowerShell:

```powershell
python -m venv .venv
```

Activate:

```powershell
.venv\Scripts\Activate.ps1
```

---

## 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

---

## 4. Configure Environment

Copy:

```text
.env.example
```

to:

```text
.env
```

Then configure:

```env
GOOGLE_API_KEY=your_api_key

DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/company_rag

EMBEDDING_MODEL=gemini-embedding-001
LLM_MODEL=gemini-3.6-flash
CHROMA_PERSIST_DIRECTORY=db/chroma
```

Never commit `.env`.

---

# Database

Create the PostgreSQL database:

```sql
CREATE DATABASE company_rag;
```

Run migrations:

```powershell
alembic upgrade head
```

Create a new migration after changing database models:

```powershell
alembic revision --autogenerate -m "describe your change"
```

Then apply it:

```powershell
alembic upgrade head
```

---

# Running the Project

The current development entry point can be started with:

```powershell
python -m app.main
```

As the project evolves, the primary application entry point will become a FastAPI application.

---

# Testing

Tests will be added progressively as each subsystem becomes stable.

The target structure is:

```text
tests/
├── unit/
│   ├── ingestion/
│   ├── indexing/
│   ├── retrieval/
│   └── generation/
│
├── integration/
│   ├── database/
│   ├── vector_store/
│   └── ingestion/
│
└── evaluation/
    └── rag/
```

The project will distinguish between:

```text
Unit Tests
Integration Tests
Evaluation Tests
End-to-End Tests
```

---

# Security

Security is considered throughout the architecture.

Planned security controls include:

* Tenant isolation
* Authentication
* Authorization
* Role-based access control
* Secure secret management
* Input validation
* Rate limiting
* Audit logging
* Secure document access
* Protection against prompt injection
* Retrieval authorization
* Prevention of cross-tenant data leakage

A critical design rule:

> Tenant identity must come from a trusted authentication context, not from an arbitrary user-provided field.

---

# Important Development Rules

Before committing changes:

```text
1. Do not commit .env
2. Do not commit API keys
3. Do not commit database files
4. Do not commit virtual environments
5. Do not commit generated caches
6. Keep migrations under version control
7. Keep application configuration separate from secrets
8. Preserve tenant isolation
9. Prefer deterministic identifiers where appropriate
10. Do not bypass domain boundaries for convenience
```

---

# Current Example Documents

The repository contains example fictional company documents under:

```text
data/documents/
```

Current examples include:

```text
hr/
├── remote_work_policy.txt
└── leave_policy.txt

security/
└── password_policy.txt
```

These documents are synthetic examples intended for development and testing.

No real company confidential information should be committed to the repository.

---

# Project Goals

The goal of this project is not merely to build a chatbot.

The goal is to understand how to design and build a **production-grade AI knowledge system**.

The project therefore focuses on questions such as:

```text
How should documents be identified?

How do we detect content changes?

How do we make indexing idempotent?

How do we isolate tenants?

How do we recover from partial failures?

How do we evaluate retrieval quality?

How do we prevent hallucinations?

How do we scale ingestion?

How do we handle duplicate jobs?

How do we retry failed operations?

How do we observe the system?

How do we deploy it?

How do we evolve the architecture without breaking existing data?
```

---

# Learning Objective

By completing this project, the target is to understand the complete lifecycle of a production RAG system:

```text
                    ┌──────────────────┐
                    │    Documents     │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │    Ingestion     │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   Processing     │
                    │   + Chunking     │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │    Embeddings    │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   Vector Store   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │    Retrieval     │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │     Reranking    │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Context Builder  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │       LLM        │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Grounded Answer  │
                    │  + Citations     │
                    └──────────────────┘
```

With production infrastructure surrounding the entire system:

```text
Authentication
       │
       ▼
     API
       │
       ├──────── PostgreSQL
       │
       ├──────── Redis
       │
       ├──────── Vector DB
       │
       ├──────── Object Storage
       │
       └──────── Message Queue
                    │
                    ▼
                  Workers
                    │
                    ▼
                Ingestion
```

---

# Project Status

Current progress:

```text
Phase 1 — Foundation              ✅
Phase 2 — Ingestion               ✅
Phase 3 — Indexing                🚧
Phase 4 — Retrieval               ⏳
Phase 5 — Generation              ⏳
Phase 6 — Evaluation              ⏳
Phase 7 — Production API          ⏳
Phase 8 — Distributed RAG         ⏳
Phase 9 — Production Infrastructure ⏳
```

The project is intentionally developed incrementally rather than implementing the entire architecture at once.

---

# License

This project is currently intended for educational and experimental purposes.

License information will be added as the project is prepared for public release.

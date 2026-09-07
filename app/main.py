from pathlib import Path

from app.core.config import settings
from app.ingestion.service import DocumentIngestionService
from app.indexing.embeddings import GeminiEmbeddingProvider
# from app.indexing.embeddings import GeminiEmbeddingProvider
from app.indexing.vector_store import ChromaVectorStore


def main() -> None:
    print("RAG system started...")

    print(f"\nEmbedding Model -> : {settings.embedding_model_name}")
    print(f"LLM Model -> : {settings.model_name}")

    print("#" * 50)

    service = DocumentIngestionService()

    documents_to_ingest = [
            {
                "file_path": Path(
                    "data/documents/hr/remote_work_policy.txt"
                ),
                "department": "hr",
                "document_type": "policy",
            },
            {
                "file_path": Path(
                    "data/documents/hr/leave_policy.txt"
                ),
                "department": "hr",
                "document_type": "policy",
            },
            {
                "file_path": Path(
                    "data/documents/security/password_policy.txt"
                ),
                "department": "security",
                "document_type": "policy",
            },
        ]
    all_chunks = []
    for document in documents_to_ingest:

        chunks = service.ingest_file(
            file_path=document["file_path"],
            tenant_id="acme",
            department=document["department"],
            document_type=document["document_type"],
            version="1",
        )

        all_chunks.extend(chunks)

    print("\n--- Ingestion Complete ---")
    print(f"Total chunks: {len(all_chunks)}")


    for index, chunk in enumerate(all_chunks):
        print("\n" + "=" * 50)
        print(f"Chunk #{index}")
        print("=" * 50)

        print("\nContent:")
        print(chunk.page_content)

        print("\nMetadata:")
        print(chunk.metadata)
        
    embedding_provider = GeminiEmbeddingProvider()

    vector_store = ChromaVectorStore(
        embedding_provider=embedding_provider,
    )

    vector_store.add_documents(all_chunks)

    print("\n--- Indexing Complete ---")
    print(f"Indexed chunks: {len(all_chunks)}")

    queries = [
        "How many days can employees work remotely?",
        "How many paid annual leave days do employees receive?",
        "Is multi-factor authentication required?",
    ]
  
    for query in queries:

        print("\n" + "#" * 60)
        print(f"QUERY: {query}")
        print("#" * 60)

        results = vector_store.similarity_search_with_scores(
            query=query,
            k=3,
            tenant_id="acme",
        )

    for index, (result, score) in enumerate(results):

            print("\n" + "-" * 50)
            print(f"Result #{index + 1}")
            print("-" * 50)

            print("\nContent:")
            print(result.page_content)

            print("\nMetadata:")
            print(result.metadata)

            print(f"Distance: {score}")

if __name__ == "__main__":
    main()
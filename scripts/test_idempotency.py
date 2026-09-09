import asyncio
from pathlib import Path

from app.database.session import AsyncSessionLocal
from app.indexing.embeddings import GeminiEmbeddingProvider
from app.indexing.vector_store import ChromaVectorStore
from app.ingestion.orchestrator import IngestionOrchestrator
from app.ingestion.repository import DocumentRepository


async def main() -> None:

    file_path = Path(
        "data/documents/engineering/test.txt"
    )

    embedding_provider = (
        GeminiEmbeddingProvider()
    )

    vector_store = ChromaVectorStore(
        embedding_provider=embedding_provider
    )

    async with AsyncSessionLocal() as session:

        repository = DocumentRepository(
            session=session
        )

        orchestrator = IngestionOrchestrator(
            repository=repository,
            vector_store=vector_store,
        )

        print("\n--- FIRST INGESTION ---")

        await orchestrator.ingest_file(
            file_path=file_path,
            tenant_id="plant",
            department="fruits",
            document_type="eat",
        )

        print("\n--- SECOND INGESTION ---")

        await orchestrator.ingest_file(
            file_path=file_path,
            tenant_id="plant",
            department="fruits",
            document_type="eat",
        )


if __name__ == "__main__":
    asyncio.run(main())
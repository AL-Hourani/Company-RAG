from pathlib import Path

from app.indexing.vector_store import ChromaVectorStore
from app.ingestion.repository import DocumentRepository
from app.ingestion.service import DocumentIngestionService
from sqlalchemy import select
from app.database.models import DocumentVersion


class IngestionOrchestrator:

    def __init__(
        self,
        repository: DocumentRepository,
        vector_store: ChromaVectorStore,
    ) -> None:

        self.repository = repository

        self.ingestion_service = (
            DocumentIngestionService(
                repository=repository
            )
        )

        self.vector_store = vector_store

    async def ingest_file(
        self,
        file_path: Path,
        tenant_id: str,
        department: str,
        document_type: str,
    ) -> None:

        chunks = await self.ingestion_service.prepare_file(
            file_path=file_path,
            tenant_id=tenant_id,
            department=department,
            document_type=document_type,
        )

        if not chunks:

            return

        document_id = chunks[0].metadata[
            "document_id"
        ]

        version_id = chunks[0].metadata[
            "version_id"
        ]

        version = await self._get_version(
            version_id
        )

        try:

            self.vector_store.add_documents(
                chunks
            )

            await self.repository.update_version_status(
                version=version,
                status="indexed",
            )

            await self.repository.session.commit()

            print(
                f"Indexed document version: "
                f"{version_id}"
            )

        except Exception as exc:

            await self.repository.update_version_status(
                version=version,
                status="failed",
                error_message=str(exc),
            )

            await self.repository.session.commit()

            raise

    async def _get_version(
        self,
        version_id: str,
    ):

        result = await self.repository.session.execute(
            select(DocumentVersion).where(
                DocumentVersion.id == version_id
            )
        )

        return result.scalar_one()
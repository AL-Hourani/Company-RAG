from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Document, DocumentVersion


class DocumentRepository:

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session

    async def get_document(
        self,
        tenant_id: str,
        filename: str,
    ) -> Document | None:

        result = await self.session.execute(
            select(Document).where(
                Document.tenant_id == tenant_id,
                Document.filename == filename,
            )
        )

        return result.scalar_one_or_none()

    async def get_latest_version(
        self,
        document_id: str,
    ) -> DocumentVersion | None:

        result = await self.session.execute(
            select(DocumentVersion)
            .where(
                DocumentVersion.document_id == document_id
            )
            .order_by(
                DocumentVersion.version_number.desc()
            )
            .limit(1)
        )

        return result.scalar_one_or_none()

    async def get_version_by_checksum(
        self,
        document_id: str,
        checksum: str,
    ) -> DocumentVersion | None:

        result = await self.session.execute(
            select(DocumentVersion).where(
                DocumentVersion.document_id == document_id,
                DocumentVersion.checksum == checksum,
            )
        )

        return result.scalar_one_or_none()

    async def create_document(
        self,
        tenant_id: str,
        filename: str,
        department: str,
        document_type: str,
    ) -> Document:

        document = Document(
            tenant_id=tenant_id,
            filename=filename,
            department=department,
            document_type=document_type,
        )

        self.session.add(document)

        await self.session.flush()

        return document

    async def create_version(
        self,
        document_id: str,
        version_number: int,
        checksum: str,
        status: str,
    ) -> DocumentVersion:

        version = DocumentVersion(
            document_id=document_id,
            version_number=version_number,
            checksum=checksum,
            status=status,
        )

        self.session.add(version)

        await self.session.flush()

        return version

    async def update_version_status(
        self,
        version: DocumentVersion,
        status: str,
        error_message: str | None = None,
    ) -> None:

        version.status = status
        version.error_message = error_message

        await self.session.flush()
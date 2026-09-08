import asyncio

from app.database.session import AsyncSessionLocal
from app.ingestion.repository import DocumentRepository


async def main() -> None:

    async with AsyncSessionLocal() as session:

        repository = DocumentRepository(
            session=session
        )

        document = await repository.create_document(
            tenant_id="acme",
            filename="remote_work_policy.txt",
            department="hr",
            document_type="policy",
        )

        await session.commit()

        print("Document created:")
        print(f"ID: {document.id}")
        print(f"Tenant: {document.tenant_id}")
        print(f"Filename: {document.filename}")


if __name__ == "__main__":
    asyncio.run(main())
from pathlib import Path

from langchain_core.documents import Document

from app.ingestion.chunker import DocumentChunker
from app.ingestion.loaders import load_text_document
from app.ingestion.identity import calculate_file_checksum
from app.ingestion.identity import create_document_id
from app.ingestion.identity import (
    calculate_file_checksum,
    create_chunk_id,
)
from app.ingestion.repository import DocumentRepository
from app.ingestion.loaders import load_text_document


class DocumentIngestionService:

    def __init__(self ,
        repository: DocumentRepository,) -> None:
        self.repository = repository
        
        self.chunker = DocumentChunker(
            chunk_size=800,
            chunk_overlap=100,
        )

    
    
    async def prepare_file(self, 
        file_path: Path,
        tenant_id: str,
        department: str,
        document_type: str) -> list[Document]:
        
        checksum = calculate_file_checksum(file_path)
        
        filename = file_path.name

        document = await self.repository.get_document(
            tenant_id=tenant_id,
            filename=filename
        )
        
        
        # case 1 file not exist
        
        if document is None:
            document = await self.repository.create_document(
                tenant_id=tenant_id,
                filename=filename,
                department=department,
                document_type=document_type
            )
            
            version_number = 1
        
        # case 2 document already exist
        
        else:
            
            latest_version = (
                await self.repository.get_latest_version(
                    document_id=document.id
                )
            )
            
            if latest_version is not None:
                if latest_version.checksum == checksum:
                    
                    print(
                        f"Skipping unchanged document: "
                        f"{filename}"
                    )

                    return []
                
                version_number = (
                    latest_version.version_number + 1
                )

            else:

                version_number = 1

        # -------------------------------------------------
        # Create new version
        # -------------------------------------------------

        version = await self.repository.create_version(
            document_id=document.id,
            version_number=version_number,
            checksum=checksum,
            status="processing",
        )
        
    
        documents = load_text_document(
            file_path=file_path,
            tenant_id=tenant_id,
            department=department,
            document_type=document_type,
            version=str(version_number),
        )

        for document_page in documents:

            document_page.metadata.update(
                {
                    "checksum": checksum,
                    "document_id": document.id,
                    "version_id": version.id,
                    "version_number": version_number,
                }
            )

        chunks = self.chunker.split(
            documents
        )

        for index, chunk in enumerate(chunks):

            chunk.metadata["chunk_index"] = index

            chunk.metadata["chunk_id"] = (
                create_chunk_id(
                    document_id=document.id,
                    version_number=version_number,
                    chunk_index=index,
                )
            )

        return chunks
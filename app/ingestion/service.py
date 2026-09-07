from pathlib import Path

from langchain_core.documents import Document

from app.ingestion.chunker import DocumentChunker
from app.ingestion.loaders import load_text_document
from app.ingestion.identity import calculate_file_checksum
from app.ingestion.identity import create_document_id

class DocumentIngestionService:

    def __init__(self) -> None:
        self.chunker = DocumentChunker(
            chunk_size=800,
            chunk_overlap=100,
        )

    def ingest_file(
        self,
        file_path: Path,
        tenant_id: str,
        department: str,
        document_type: str,
        version: str = "1",
    ) -> list[Document]:


        checksum = calculate_file_checksum(file_path)
        document_id = create_document_id(
            tenant_id=tenant_id,
            checksum=checksum,
        )
        documents = load_text_document(
            file_path=file_path,
            tenant_id=tenant_id,
            department=department,
            document_type=document_type,
            version=version,
        )
        
        for document in documents:
            document.metadata.update(
                {
                    "checksum": checksum,
                    "document_id": document_id,
                }
            )

        chunks = self.chunker.split(documents)
        for index, chunk in enumerate(chunks):
            chunk.metadata["chunk_index"] = index

            chunk.metadata["chunk_id"] = (
                f"{document_id}:chunk:{index}"
            )

        return chunks
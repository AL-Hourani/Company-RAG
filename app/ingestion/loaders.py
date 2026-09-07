

from pathlib import Path
from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader



def load_text_document(
    file_path : Path ,
    tenant_id : str,
    department: str,
    document_type: str,
    version: str = "1"
) -> list[Document]:
    
    loader = TextLoader(
        file_path=file_path ,
        encoding="utf-8"
    )
    
    documents = loader.load()
    for document in documents:
            document.metadata.update(
                {
                    "tenant_id": tenant_id,
                    "filename": file_path.name,
                    "source": str(file_path),
                    "content_type": "text/plain",
                    "department": department,
                    "document_type": document_type,
                    "version": version,
                }
            )
    
    return documents
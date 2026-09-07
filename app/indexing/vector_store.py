


from langchain_chroma import Chroma
from app.core.config import settings
from app.indexing.embeddings import GeminiEmbeddingProvider
from langchain_core.documents import Document

class ChromaVectorStore:
    
    def __init__(self ,
        embedding_provider: GeminiEmbeddingProvider):
        
        self._store = Chroma(
             collection_name="company_documents",
             embedding_function=embedding_provider.model,
             persist_directory=settings.chroma_persist_directory
        )
        
    
    def add_documents(self , 
        documents : list[Document]) -> None:
        ids = [
            document.metadata["chunk_id"]
            for document in documents
        ]
        
        self._store.add_documents(
            documents=documents,
            ids = ids
        )
        
    
    
    
    def similarity_search(
        self,
        query: str,
        k: int = 5,
        tenant_id: str | None = None,
    ) -> list[Document]:

        filter_metadata = None

        if tenant_id is not None:
            filter_metadata = {
                "tenant_id": tenant_id,
            }

        return self._store.similarity_search(
            query=query,
            k=k,
            filter=filter_metadata,
        )

    def similarity_search_with_scores(
        self,
        query: str,
        k: int = 5,
        tenant_id: str | None = None,
    ) -> list[tuple[Document, float]]:

        filter_metadata = None

        if tenant_id is not None:
            filter_metadata = {
                "tenant_id": tenant_id,
            }

        return self._store.similarity_search_with_score(
            query=query,
            k=k,
            filter=filter_metadata,
        )
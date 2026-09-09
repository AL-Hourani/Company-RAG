


from langchain_chroma import Chroma
from app.core.config import settings
from app.indexing.embeddings import GeminiEmbeddingProvider
from langchain_core.documents import Document
from app.core.retrieval import RetrievalFilter

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
        filters : RetrievalFilter,
        k: int = 5
    ) -> list[Document]:


        filter_metadata = self._build_filter(
            filters
        )
        return self._store.similarity_search(
            query=query,
            k=k,
            filter=filter_metadata,
        )

    def similarity_search_with_scores(
        self,
        query: str,
        filters : RetrievalFilter,
        k: int = 5
    ) -> list[tuple[Document, float]]:


        filter_metadata = self._build_filter(
            filters
        )

        return self._store.similarity_search_with_score(
            query=query,
            k=k,
            filter=filter_metadata,
        )
        
    def _build_filter(
        self , 
        filters : RetrievalFilter
    ) -> dict:
        
        metadata_filter = {
            "tenant_id":filters.tenant_id
        }
        
        if filters.department:
            metadata_filter["department"]= (
                filters.department
            )
            
        if filters.document_type:
            metadata_filter["document_type"]= (
                filters.document_type
            )
            
        if filters.document_id:
            metadata_filter["document_id"]= (
                filters.document_id
            )
        
        if filters.version_number:
            metadata_filter["version_number"]= (
                filters.version_number
            )
        
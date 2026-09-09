from langchain_core.documents import Document

from app.indexing.vector_store import ChromaVectorStore
from app.core.retrieval import (
    RetrievalFilter,
    RetrievalStrategy,
    RetrievedDocument,
)

class DocumentRetriever:

    def __init__(
        self,
        vector_store: ChromaVectorStore,
    ) -> None:

        self.vector_store = vector_store

    def retrieve(
        self,
        query: str,
        filters : RetrievalFilter,
        strategy : RetrievalStrategy = (
            RetrievalStrategy.DENSE
        ),
        k: int = 5,
        fetch_k = 20
    ) -> list[Document]:

        if strategy == RetrievalStrategy.DENSE:
            return self.vector_store.similarity_search(
                query=query,
                k=k,
                filters=filters
            )
        
        
        if strategy == RetrievalStrategy.MMR:

            return (
                self.vector_store
                .max_marginal_relevance_search(
                    query=query,
                    k=k,
                    fetch_k=fetch_k,
                    filters=filters,
                )
            )

        raise ValueError(
            f"Unsupported retrieval strategy: "
            f"{strategy}"
        )
    
    
    
    def retrieve_with_scores(
        self,
        query: str,
        filters: RetrievalFilter,
        k: int = 5,
    ) -> list[RetrievedDocument]:

        results = (
            self.vector_store
            .similarity_search_with_scores(
                query=query,
                k=k,
                filters=filters,
            )
        )

        return [
            RetrievedDocument(
                document=document,
                distance=distance,
            )
            for document, distance in results
        ]
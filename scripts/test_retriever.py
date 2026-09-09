from app.core.retrieval import RetrievalFilter
from app.indexing.embeddings import GeminiEmbeddingProvider
from app.indexing.vector_store import ChromaVectorStore
from app.retrieval.retriever import DocumentRetriever


def main() -> None:

    embedding_provider = (
        GeminiEmbeddingProvider()
    )

    vector_store = ChromaVectorStore(
        embedding_provider=embedding_provider
    )

    retriever = DocumentRetriever(
        vector_store=vector_store
    )

    filters = RetrievalFilter(
        tenant_id="plant",
    )

    query = (
        "what are leaves of banana plants look like ?"
    )

    documents = retriever.retrieve(
        query=query,
        filters=filters,
        k=3,
    )

    print("\n--- Retrieval Results ---")

    for index, document in enumerate(
        documents,
        start=1,
    ):

        print(f"\nResult #{index}")
        print(document.page_content)
        print(document.metadata)


if __name__ == "__main__":
    main()
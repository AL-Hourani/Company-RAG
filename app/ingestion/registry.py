


# just a simple registry before using a database like (postgres)
from app.ingestion.domain.models import DocumentRecord


class DocumentRegistry:

    def __init__(self) -> None:
        self._documents: dict[str, DocumentRecord] = {}

    def get(
        self,
        document_id: str,
    ) -> DocumentRecord | None:

        return self._documents.get(document_id)

    def save(
        self,
        document: DocumentRecord,
    ) -> None:

        self._documents[document.document_id] = document
    

    def exists(
            self,
            document_id: str,
        ) -> bool:

            return document_id in self._documents
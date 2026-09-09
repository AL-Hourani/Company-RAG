from dataclasses import dataclass
from enum import Enum
from langchain_core.documents import Document


class RetrievalStrategy(str , Enum):
    DENSE = "dense"
    MMR = "mmr"


@dataclass(frozen=True)
class RetrievalFilter:
    tenant_id:str
    department : str | None = None
    document_type : str | None = None
    document_id : str | None = None
    version_number : int | None = None
    
    
    
@dataclass(frozen=True)
class RetrievedDocument:
    document: Document
    distance: float
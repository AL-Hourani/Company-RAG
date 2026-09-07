

from dataclasses import dataclass
from enum import Enum


class DocumentStatus(str, Enum):
    NEW = "new"
    PROCESSING = "processing"
    INDEXED = "indexed"
    FAILED = "failed"


@dataclass
class DocumentRecord:
    document_id: str
    tenant_id: str
    filename: str
    checksum: str
    version: str
    status: DocumentStatus
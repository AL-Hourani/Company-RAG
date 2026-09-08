

import hashlib
from pathlib import Path



def calculate_file_checksum(file_path : Path):
    sha256 = hashlib.sha256()
    
    with file_path.open("rb") as file:
        while chunk := file.read(8192):
            sha256.update(chunk)
    
    return sha256.hexdigest()




def create_document_id(
    tenant_id: str,
    checksum: str,
) -> str:
    raw_id = f"{tenant_id}:{checksum}"

    return hashlib.sha256(
        raw_id.encode("utf-8")
    ).hexdigest()
    

def create_chunk_id(
    document_id: str,
    version_number: int,
    chunk_index: int,
) -> str:

    return (
        f"{document_id}:"
        f"v{version_number}:"
        f"chunk:{chunk_index}"
    )
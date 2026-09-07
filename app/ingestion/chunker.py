


from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter



class DocumentChunker:
    
    def __init__(self ,
                 chunk_size : int = 800,
                 chunk_overlap : int = 100
                 ):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[
                "\n",
                "\n\n"
                ".",
                " ",
                ""
            ]
        )
    
    def split(self, documents : list[Document])-> list[Document]:
        
        chunks = self.splitter.split_documents(documents)
        
        
        return chunks
    
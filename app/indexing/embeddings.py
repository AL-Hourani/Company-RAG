


from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.core.config import settings



class GeminiEmbeddingProvider:
    
    def __init__(self) -> None:
        self._model = GoogleGenerativeAIEmbeddings(
            model = settings.embedding_model_name,
            api_key=settings.gemini_api_key
        )
        
    @property
    def model(self) -> GoogleGenerativeAIEmbeddings:
         return self._model

    def embed_documents(self , 
        texts : list[str]) -> list[list[float]]:
        
        return self._model.embed_documents(texts)
    
    def embed_query(
        self,
        text: str,
    ) -> list[float]:

        return self._model.embed_query(text)
    
    
 
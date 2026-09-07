



from functools import lru_cache
from pydantic_settings import BaseSettings , SettingsConfigDict


class Settings(BaseSettings):
    
    gemini_api_key : str
    
    model_name : str
    
    embedding_model_name : str
    
    chroma_persist_directory : str = "db/chroma"
    
    database_url : str
    
    alembic_database_url : str
    
    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )
    

@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
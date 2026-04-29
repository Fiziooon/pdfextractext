from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    mongo_initdb_root_username: str
    mongo_initdb_root_password: str
    
    mongo_url: str = "mongodb://localhost:27017"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')

settings = Settings()
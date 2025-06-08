from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # PostgreSQL
    POSTGRES_HOST: str 
    POSTGRES_PORT: int = 5432

    # MongoDB
    MONGO_DB: str
    MONGO_HOST: str
    MONGO_PORT: int = 27017

    # Redis
    REDIS_HOST: str
    REDIS_PORT: int = 6379

    # Ngrok / WebSocket
    FASTAPI_PORT: int = 8000
    WEBSOCKET_PORT: int = 8000
    NGROK_AUTH_TOKEN: str

    # Github:
    VITE_GITHUB_GIST_ID: str
    GITHUB_TOKEN: str

    class Config:
        env_file = ".env"

settings = Settings()

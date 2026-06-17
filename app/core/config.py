from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str
    DEBUG: bool

    DATABASE_URL: str
    checkpointers_db:str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    # api_token: str
    # model_id: str
    GROQ_API_KEY: str
    GROQ_MODEL: str

    GOOGLE_API_KEY: str

    MAX_FILE_SIZE_MB: int

    class Config:
        env_file = ".env"


settings = Settings()
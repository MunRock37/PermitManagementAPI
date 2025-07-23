from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    redis_broker_url: str
    secret_key: str

    class Config:
        env_file = ".env"


settings = Settings()

from functools import lru_cache

from fastapi.security import OAuth2PasswordBearer
from pydantic import PostgresDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    APP_NAME: str = "Booknotes"
    API_VERSION: str = "/v1"
    TOKEN_URL: str = API_VERSION + "/login"

    oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl=TOKEN_URL)

    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr

    JWT_SECRET_KEY: SecretStr
    JWT_ALGORITHM: str

    def assemble_database_uri(self):
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD.get_secret_value(),
            host=self.POSTGRES_HOST,
            port=int(self.POSTGRES_PORT),
            path=f"{self.POSTGRES_DB}",
        ).unicode_string()


@lru_cache
def get_config():
    return Settings()


config = get_config()

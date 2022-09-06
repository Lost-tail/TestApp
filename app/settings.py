
from pydantic import BaseSettings


class Settings(BaseSettings):

    PROJECT_NAME: str

    SHEET_ID: str
    TOKEN_FILE_PATH: str

    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
                                                                                                                                                         
    class Config:
        case_sensitive = True


settings = Settings(_env_file='.env', _env_file_encoding='utf-8')
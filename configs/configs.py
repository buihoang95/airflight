from typing import Optional

from pydantic_settings import BaseSettings

class Config(BaseSettings):
    FLIGHTAPI_KEY: Optional[str] = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

app_configs = Config()
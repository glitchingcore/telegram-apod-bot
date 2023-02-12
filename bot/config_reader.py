from pydantic import BaseSettings, SecretStr, validator


class Settings(BaseSettings):
    bot_token: SecretStr
    nasa_api_token: SecretStr
    channel_username: str

    @validator("channel_username")
    def validate_channel_username(cls, value):
        if not value.startswith("@"):
            raise ValueError("Incorrect 'channel_username' values. Must start with '@'")
        return value

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


config = Settings()

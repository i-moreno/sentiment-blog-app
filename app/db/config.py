from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env.dev", env_file_encoding="utf-8")

    db_user: str
    db_password: SecretStr
    db_host: str
    db_port: int
    db_name: str

    @property
    def database_url(self) -> str:
        password = self.db_password.get_secret_value()
        db_url = f"postgresql+psycopg2://{self.db_user}:{password}@{self.db_host}:{self.db_port}/{self.db_name}"
        return db_url

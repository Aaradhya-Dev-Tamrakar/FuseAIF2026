from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int
    postgres_db: str
    
    secret_key: str
    debug: bool = False

    # Tell pydantic to load variables from our .env file
    # It will automatically match them to the variables above (case-insensitive)
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

# Create a global settings object that is initialized once
settings = Settings()

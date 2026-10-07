from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "SkillSetu"
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    DATABASE_URL: str = "sqlite:///./skillsetu.db"
    ENVIRONMENT: str = "development"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


settings = Settings()

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )

    # 应用配置
    app_name: str = "剧本杀系统API"
    app_version: str = "1.0.0"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000

    # JWT配置
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # MongoDB配置
    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "script_kill_ai"

    # 日志配置
    log_level: str = "INFO"


settings = Settings()


# 定义依赖函数
def get_settings() -> Settings:
    return settings

"""FastAPI server configuration."""

import dataclasses
import logging
import logging.config
import os
from pathlib import Path

import dotenv
from singleton import Singleton

dotenv.load_dotenv()


@dataclasses.dataclass
class Settings(metaclass=Singleton):
    """Server config settings."""

    base_dir: Path = Path(__file__).resolve().parent.parent
    root_url: str = os.getenv("DOMAIN", default="http://localhost:8000")
    project_name: str = os.getenv("PROJECT_NAME", default="PROJECT")
    base_path: str = "/api/v1"
    worker_update_time: int = int(os.getenv("WORKER_UPDATE_TIME", default=180))
    testing: bool = os.getenv("DEBUG", default=False)

    page_max_limit: int = 100

    mongo_uri: str = os.getenv("MONGO_URI", default="mongodb://localhost:27017/")
    redis_uri: str = os.getenv("REDIS_URI", default="redis://localhost:6379/0")

    app_id: str = os.getenv("APP_ID")
    app_secret: str = os.getenv("APP_SECRET")

    JWT_CONFIG: str = os.getenv(
        "USSO_JWT_CONFIG",
        default='{"jwk_url": "https://sso.usso.io/website/jwks.json","type": "RS256","header": {"type": "Cookie", "name": "usso_access_token"} }',
    )

    log_config = {
        "version": 1,
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "standard",
            },
            "file": {
                "class": "logging.FileHandler",
                "level": "INFO",
                "filename": base_dir / "logs" / "info.log",
                "formatter": "standard",
            },
        },
        "formatters": {
            "standard": {
                "format": "[{levelname} : {filename}:{lineno} : {asctime} -> {funcName:10}] {message}",
                "style": "{",
            }
        },
        "loggers": {
            "": {"handlers": ["console", "file"], "level": "INFO", "propagate": True}
        },
    }

    @classmethod
    def config_logger(cls):
        if not (cls.base_dir / "logs").exists():
            (cls.base_dir / "logs").mkdir()

        logging.config.dictConfig(cls.log_config)
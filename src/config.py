import logging
import os
from functools import lru_cache
from typing import Optional

import sentry_sdk
from pydantic import BaseSettings, Field
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration

logger = logging.getLogger(__name__)

ENV_PREFIX = 'NOTIFYME_'
ENV_FILENAME_POSTFIX = '_FILE'
DEFAULT_URL_SETTING_NAME = 'NOTIFYME_DEFAULT'


def get_notify_urls() -> dict[str, str]:
    envs = {}
    for env in os.environ:
        if env.startswith(ENV_PREFIX) and env.endswith(ENV_FILENAME_POSTFIX):
            with open(env, 'r') as secret_file:
                envs[env.strip(ENV_FILENAME_POSTFIX)] = secret_file.read()
        elif env.startswith(ENV_PREFIX):
            envs[env] = os.environ[env]
    return envs


class Settings(BaseSettings):
    urls: dict[str, str] = get_notify_urls()
    sentry_dsn: Optional[str] = Field(env='sentry_dsn', default=None)
    environment: Optional[str] = Field(env='environment', default='production')

    class Config:
        secrets_dir = '/run/secrets'


@lru_cache()
def get_settings() -> Settings:
    logger.info("Loading config settings from the environment...")
    return Settings()


settings = get_settings()

if settings.sentry_dsn:
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        integrations=[
            StarletteIntegration(transaction_style="endpoint"),
            FastApiIntegration(transaction_style="endpoint"),
        ],
        environment=settings.environment,
    )

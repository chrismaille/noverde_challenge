"""Configure Sentry."""
import os

import sentry_sdk
from loguru import logger
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration


def configure_sentry() -> bool:
    """Configure Sentry."""
    dsn = os.getenv("SENTRY_DSN")
    if dsn:
        env = os.getenv("SENTRY_ENV")
        sentry_sdk.init(  # type: ignore
            dsn=dsn, integrations=[AwsLambdaIntegration()], environment=env
        )
        logger.info(f"Sentry initialized.")
        return True
    else:
        logger.warning("Sentry not available.")
        return False

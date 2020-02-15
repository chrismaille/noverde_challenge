"""Get Secrets Module."""
import os
from typing import Optional

from loguru import logger


def get_secret(secret: str) -> Optional[str]:
    """Get Secrets.

    For this challenge we will use Environment variables.

    In production settings, its safer to use solutions
    like AWS Secrets Manager or AWS Systems Manager Parameter Service.

    :param secret: AWS SM Parameter Service qualified name
    :return: string
    """
    env_name = secret.replace("/", "_").upper()[1:]
    logger.debug(f"Looking for env {env_name}")
    return os.getenv(env_name)

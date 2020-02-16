"""Noverde Challenge Package."""
from noverde_challenge.utils.debug import set_remote_debug
from noverde_challenge.utils.sentry import configure_sentry

__version__ = "0.1.0"

set_remote_debug()
configure_sentry()

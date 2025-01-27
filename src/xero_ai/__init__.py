from .__main__ import main

import logfire

from .settings import LOGFIRE_SERVICE_NAME

__all__ = ["main", "xero_ai"]

logfire.configure(
    send_to_logfire="if-token-present",
    service_name=LOGFIRE_SERVICE_NAME,
)

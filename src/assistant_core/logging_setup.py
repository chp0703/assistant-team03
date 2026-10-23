"""JSON logging configuration for the assistant service."""

from __future__ import annotations

import json
import logging
import sys
from typing import TextIO

_LOGGER_NAME = "assistant_core"
_SAFE_EXTRA_FIELDS = ("intent", "latency_ms", "session", "degraded")


class JsonFormatter(logging.Formatter):
    """Format log records as compact JSON with an explicit safe field set."""

    def format(self, record: logging.LogRecord) -> str:
        data: dict[str, object] = {
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        for field in _SAFE_EXTRA_FIELDS:
            if hasattr(record, field):
                data[field] = getattr(record, field)
        return json.dumps(data, ensure_ascii=False, default=str)


def setup_logging(level: str = "INFO", *, stream: TextIO | None = None) -> logging.Logger:
    """Configure the assistant logger to emit JSON records to stderr.

    ``stream`` is injectable so callers can direct output when needed. Repeated
    calls update the existing handler instead of adding duplicate output.
    """
    logger = logging.getLogger(_LOGGER_NAME)
    logger.setLevel(level.upper())
    logger.propagate = False

    handler = next(
        (item for item in logger.handlers if getattr(item, "_assistant_json_handler", False)),
        None,
    )
    if handler is None:
        handler = logging.StreamHandler(stream if stream is not None else sys.stderr)
        handler._assistant_json_handler = True  # type: ignore[attr-defined]
        logger.addHandler(handler)
    elif stream is not None:
        handler.setStream(stream)

    handler.setFormatter(JsonFormatter())
    return logger

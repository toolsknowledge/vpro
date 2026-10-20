"""Structured (key=value) logging configuration."""

import logging

LOG_FORMAT = "time=%(asctime)s level=%(levelname)s logger=%(name)s message=%(message)s"


def configure_logging(level: int = logging.INFO) -> None:
    logging.basicConfig(level=level, format=LOG_FORMAT)

import logging
import sys


def init_logging(level: int = logging.INFO):
    """Configure root logger to stdout"""
    formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    handler.setFormatter(formatter)
    root = logging.getLogger()
    root.setLevel(level)
    root.addHandler(handler)

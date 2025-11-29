from functools import wraps
import logging

logger = logging.getLogger("pipeline")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s — %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Calling {func.__name__}")
        try:
            result = func(*args, **kwargs)
            logger.info(f"{func.__name__} finished successfully")
            return result
        except Exception as e:
            logger.exception(f"{func.__name__} failed: {e}")
            raise

    return wrapper

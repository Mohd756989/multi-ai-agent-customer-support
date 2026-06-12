import logging
import os

LOG_PATH = os.path.join(os.path.dirname(__file__), "..", "logs", "application.log")
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)


def get_logger(name: str) -> logging.Logger:
    """Return a logger that writes to both console and the application log file."""
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger  # already configured

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s %(name)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # File handler
    fh = logging.FileHandler(LOG_PATH)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger

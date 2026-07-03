import logging
from pathlib import Path


# logs Folder तयार करा
log_folder = Path("logs")
log_folder.mkdir(exist_ok=True)

log_file = log_folder / "app.log"


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    filename=log_file,
    filemode="a"
)


def log_info(message):
    logging.info(message)


def log_error(message):
    logging.error(message)
import logging
import sys

from blacksheep import Application, get

stdout_handler = logging.StreamHandler(stream=sys.stdout)
logger = logging.Logger("s3-event-notifier")
logger.addHandler(stdout_handler)

app = Application(show_error_details=False)


@get("/health")
def health():
    logger.info("Health check endpoint called")
    return 200

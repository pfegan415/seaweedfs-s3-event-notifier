import json
import logging
import sys

from blacksheep import Application, FromJSON, post, get

stdout_handler = logging.StreamHandler(stream=sys.stdout)
logger = logging.Logger("s3-event-notifier")
logger.addHandler(stdout_handler)

app = Application(show_error_details=False)


@get("/health")
def health():
    logger.info("Health check endpoint called")
    return 200

@post("/webhook")
def webhook(data: FromJSON[dict]):
    logger.info(f"Received webhook with payload: {json.dumps(data.value)}")
    message = {
        "eventType": data.value["event_type"],
        "key": data.value["key"],
    }
    logger.info(f"Message: {json.dumps(message)}")
    return 200

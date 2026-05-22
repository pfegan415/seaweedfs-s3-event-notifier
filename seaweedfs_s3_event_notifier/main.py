import json
import logging
import sys

from blacksheep import Application, FromJSON, post, get
import boto3

stdout_handler = logging.StreamHandler(stream=sys.stdout)
logger = logging.Logger("s3-event-notifier")
logger.addHandler(stdout_handler)


SQS_CLIENT = boto3.client(
    "sqs",
    region_name="us-east-1",
    endpoint_url="http://localhost:9324",
    aws_access_key_id="x",
    aws_secret_access_key="x",
)

QUEUE_URL = "http://localhost:9324/000000000000/test-queue"  # TODO: replace with env var

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
    logger.info(f"Sending message to SQS queue at {QUEUE_URL}")
    SQS_CLIENT.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(message)
    )
    return 200

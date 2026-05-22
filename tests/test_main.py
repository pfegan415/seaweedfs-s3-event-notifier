import json

import boto3
import pytest
from blacksheep.contents import JSONContent
from blacksheep.testing import TestClient

from seaweedfs_s3_event_notifier.main import app


@pytest.fixture(scope="session")
async def http_client():
    await app.start()
    yield TestClient(app)
    await app.stop()


@pytest.fixture(scope="function")
def sqs_client():
    return boto3.client(
        "sqs",
        region_name="us-east-1",
        endpoint_url="http://localhost:9324",
        aws_access_key_id="x",
        aws_secret_access_key="x",
    )


@pytest.mark.asyncio
async def test_health_returns_200(http_client: TestClient):
    response = await http_client.get("/health")
    assert response.status == 200

@pytest.mark.asyncio
async def test_webhook_writes_to_queue(http_client: TestClient, sqs_client):
    sqs_client.create_queue(QueueName="test-queue")

    payload = {"event_type": "object_created", "key": "test.txt"}

    await http_client.post(
        path="/webhook",
        headers={"Content-Type": "application/json"},
        content=JSONContent(payload),
    )

    queue_messages = sqs_client.receive_message(
        QueueUrl="http://localhost:9324/000000000000/test-queue",
        MaxNumberOfMessages=10,
        WaitTimeSeconds=10,
    )

    assert json.loads(
        queue_messages.get("Messages")[0].get("Body")
    ).get("eventType") == payload["event_type"]

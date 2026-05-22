import pytest
from blacksheep.contents import JSONContent
from blacksheep.testing import TestClient

from seaweedfs_s3_event_notifier.main import app


@pytest.fixture(scope="session")
async def client():
    await app.start()
    yield TestClient(app)
    await app.stop()


@pytest.mark.asyncio
async def test_health_returns_200(client: TestClient):
    response = await client.get("/health")
    assert response.status == 200

@pytest.mark.asyncio
async def test_webhook_returns_200(client: TestClient):
    payload = {"event_type": "object_created", "key": "test.txt"}
    response = await client.post(
        path="/webhook",
        headers={"Content-Type": "application/json"},
        content=JSONContent(payload),
    )
    assert response.status == 200
import pytest
from blacksheep.testing import TestClient

from seaweedfs_s3_event_notifier.main import app


@pytest.fixture()
async def client():
    await app.start()
    yield TestClient(app)
    await app.stop()


@pytest.mark.asyncio
async def test_health_returns_200(client: TestClient):
    response = await client.get("/health")
    assert response.status == 200
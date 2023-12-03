import pytest
from httpx import AsyncClient


async def create_post(body: str, async_client: AsyncClient) -> dict:
    response = await async_client.post("/post", json={"body": body})
    return response.json()

@pytest.fixture()
# This will look at the conftest.py file getting the "ac" from the fixture async_client method
async def created_post(async_client: AsyncClient):
    return await create_post("Test post", async_client)
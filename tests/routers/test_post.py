import pytest
from httpx import AsyncClient
from fastapi import status


async def create_post(body: str, async_client: AsyncClient) -> dict:
    response = await async_client.post("/posts", json={"body": body})
    return response.json()


@pytest.fixture()
# This will look at the conftest.py file getting the "ac" from the fixture async_client method
async def created_post(async_client: AsyncClient):
    return await create_post("VODY", async_client)


@pytest.mark.anyio
async def test_create_post(async_client: AsyncClient):
    body = "Test post"

    response = await async_client.post("/posts", json={"body": body})

    assert response.status_code == status.HTTP_201_CREATED
    assert {"id": 0, "body": body}.items() <= response.json().items()


@pytest.mark.anyio
async def test_create_post_missing_data(async_client: AsyncClient):
    response = await async_client.post("/posts", json={})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.anyio
async def test_get_all_post(async_client: AsyncClient, created_post: dict):
    response = await async_client.get("/posts")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [created_post]

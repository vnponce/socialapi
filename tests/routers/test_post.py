import pytest
from httpx import AsyncClient
from fastapi import status


async def create_post(body: str, async_client: AsyncClient) -> dict:
    response = await async_client.post("/posts", json={"body": body})
    return response.json()


async def create_comment(body: str, post_id: int, async_client: AsyncClient) -> dict:
    response = await async_client.post("/comments", json={"body": body, "post_id": post_id})
    return response.json()


@pytest.fixture()
# This will look at the conftest.py file getting the "ac" from the fixture async_client method
async def created_post(async_client: AsyncClient):
    return await create_post("Post Body", async_client)


@pytest.fixture()
async def created_comment(async_client: AsyncClient, created_post: dict):
    return await create_comment("Comment Body", created_post["id"], async_client)


@pytest.mark.anyio
async def test_create_post(async_client: AsyncClient):
    body = "Test post"

    response = await async_client.post("/posts", json={"body": body})

    assert response.status_code == status.HTTP_201_CREATED
    assert {"id": 1, "body": body}.items() <= response.json().items()


@pytest.mark.anyio
async def test_create_post_missing_data(async_client: AsyncClient):
    response = await async_client.post("/posts", json={})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.anyio
async def test_get_all_post(async_client: AsyncClient, created_post: dict):
    response = await async_client.get("/posts")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [created_post]


@pytest.mark.anyio
async def test_create_comment(async_client: AsyncClient, created_post: dict):
    body = "Comment Body"
    response = await async_client.post("/comments", json={"body": body, "post_id": created_post["id"]})

    assert response.status_code == status.HTTP_201_CREATED
    assert {"id": 1, "body": body, "post_id": created_post["id"]}.items() <= response.json().items()

@pytest.mark.anyio
async def test_get_comments_on_post(async_client: AsyncClient, created_post: dict, created_comment: dict):
    response = await async_client.get(f"/posts/{created_post["id"]}/comments")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() <= [created_comment]

@pytest.mark.anyio
async def test_get_comments_on_post(async_client: AsyncClient, created_post: dict):
    response = await async_client.get(f"/posts/{created_post["id"]}/comments")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() <= []

@pytest.mark.anyio
async def test_get_post_with_comments(async_client: AsyncClient, created_post: dict, created_comment: dict):
    response = await async_client.get(f"/posts/{created_post["id"]}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"post": created_post, "comments": [created_comment]}

@pytest.mark.anyio
async def test_get_missing_post_with_comments(async_client: AsyncClient, created_post: dict, created_comment: dict):
    response = await async_client.get("/posts/2")
    assert response.status_code == status.HTTP_404_NOT_FOUND

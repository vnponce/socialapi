import pytest
from httpx import AsyncClient
from fastapi import status

import security


def bearer_headers(token):
    return {"Authorization": f"Bearer {token}"}


async def create_post(body: str, async_client: AsyncClient, logged_in_token: str) -> dict:
    response = await async_client.post("/posts", json={"body": body}, headers=bearer_headers(logged_in_token))
    return response.json()


async def create_comment(body: str, post_id: int, async_client: AsyncClient, logged_in_token: str) -> dict:
    response = await async_client.post("/comments", json={"body": body, "post_id": post_id, }, headers=bearer_headers(logged_in_token))
    return response.json()


@pytest.fixture()
# This will look at the conftest.py file getting the "ac" from the fixture async_client method
async def created_post(async_client: AsyncClient, logged_in_token: str):
    return await create_post("Post Body", async_client, logged_in_token=logged_in_token)


@pytest.fixture()
async def created_comment(async_client: AsyncClient, created_post: dict, logged_in_token: str):
    return await create_comment("Comment Body", created_post["id"], async_client, logged_in_token=logged_in_token)


@pytest.mark.anyio
async def test_create_post(async_client: AsyncClient, registered_user: dict, logged_in_token: str):
    body = "Test post"

    response = await async_client.post("/posts", json={"body": body}, headers=bearer_headers(logged_in_token))

    assert response.status_code == status.HTTP_201_CREATED
    assert {"id": 1, "body": body, "user_id": registered_user["id"]}.items() <= response.json().items()


@pytest.mark.anyio
async def test_create_post_expired_token(
        async_client: AsyncClient, registered_user: dict, mocker
):
    mocker.patch("security.access_token_expire_minutes", return_value=-1)
    token = security.create_access_token(registered_user["email"])
    response = await async_client.post(
        "/posts",
        json={"body": "Test post"},
        headers=bearer_headers(token)
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Token has expired" in response.json()["detail"]


@pytest.mark.anyio
async def test_create_post_missing_data(async_client: AsyncClient, logged_in_token: str):
    response = await async_client.post("/posts", json={}, headers=bearer_headers(logged_in_token))

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.anyio
async def test_get_all_post(async_client: AsyncClient, created_post: dict):
    response = await async_client.get("/posts")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [created_post]


@pytest.mark.anyio
async def test_create_comment(async_client: AsyncClient, created_post: dict, registered_user: dict,  logged_in_token: str):
    body = "Comment Body"
    response = await async_client.post("/comments", json={"body": body, "post_id": created_post["id"]}, headers=bearer_headers(logged_in_token))

    assert response.status_code == status.HTTP_201_CREATED
    assert {"id": 1, "body": body, "post_id": created_post["id"], "user_id": registered_user["id"]}.items() <= response.json().items()


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

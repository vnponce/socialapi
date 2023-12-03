from typing import List

from fastapi import APIRouter, HTTPException, status

from database import comment_table, post_table, database
from models.post import UserPost, UserPostIn, Comment, CommentIn, UserPostWithComments

router = APIRouter()


async def find_post(post_id: int):
    query = post_table.select().where(post_table.c.id == post_id)
    return await database.fetch_one(query)


@router.post("/posts", response_model=UserPost, status_code=status.HTTP_201_CREATED)
async def create_post(post: UserPostIn):
    data = post.model_dump()
    query = post_table.insert().values(data)
    last_record_id = await database.execute(query)
    return {**data, "id": last_record_id}


@router.get("/posts", response_model=List[UserPost])
async def get_posts():
    query = post_table.select()
    return await database.fetch_all(query)


@router.get("/posts/{post_id}/comments", response_model=List[Comment])
async def get_comments_on_post(post_id: int):
    query = comment_table.select().where(comment_table.c.post_id == post_id)
    return await database.fetch_all(query)


@router.get("/posts/{post_id}", response_model=UserPostWithComments)
async def get_post_with_comments(post_id: int):
    post = await find_post(post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found!")

    return {
        "post": post,
        "comments": await get_comments_on_post(post_id)
    }


@router.post("/comments", response_model=Comment, status_code=status.HTTP_201_CREATED)
async def create_post(comment: CommentIn):
    post = await find_post(comment.post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found!")

    data = comment.model_dump()
    query = comment_table.insert().values(data)
    last_record_id = await database.execute(query)
    return {**data, "id": last_record_id}


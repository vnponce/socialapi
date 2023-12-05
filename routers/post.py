from typing import List, Annotated

from fastapi import APIRouter, HTTPException, status, Request, Depends

from database import comment_table, post_table, database, like_table
from models.post import UserPost, UserPostIn, Comment, CommentIn, UserPostWithComments, PostLIkeIn, PostLIke
from models.user import User
# oauth2_scheme reads the Request headers to find the Authorization value "Bearer [token]"
from security import get_current_user, oauth2_scheme

router = APIRouter()


async def find_post(post_id: int):
    query = post_table.select().where(post_table.c.id == post_id)
    return await database.fetch_one(query)


@router.post("/posts", response_model=UserPost, status_code=status.HTTP_201_CREATED)
async def create_post(post: UserPostIn, current_user: Annotated[User, Depends(get_current_user)]):
    data = {**post.model_dump(), "user_id": current_user.id}
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
async def create_post(comment: CommentIn, request: Request, current_user: Annotated[User, Depends(get_current_user)]):
    post = await find_post(comment.post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found!")

    data = {**comment.model_dump(), "user_id": current_user.id}
    query = comment_table.insert().values(data)
    last_record_id = await database.execute(query)
    return {**data, "id": last_record_id}


@router.post("/like", response_model=PostLIke, status_code=status.HTTP_201_CREATED)
async def like_post(like: PostLIkeIn, current_user: Annotated[User, Depends(get_current_user)]):
    post = await find_post(like.post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found!")

    data = {**like.model_dump(), "user_id": current_user.id}
    query = like_table.insert().values(data)

    last_record_id = await database.execute(query)
    return {"id": last_record_id, **data}

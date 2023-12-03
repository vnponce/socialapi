from typing import List

from fastapi import APIRouter

from models.post import UserPost, UserPostIn

router = APIRouter()

post_table = {}


@router.post("/posts", response_model=UserPost)
async def create_post(post: UserPostIn):
    data = post.model_dump()
    last_record_id = len(post_table)
    new_post = {**data, "id": last_record_id}
    post_table[last_record_id] = new_post
    return new_post


@router.get("/posts", response_model=List[UserPost])
async def get_posts():
    return list(post_table.values())

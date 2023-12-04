from fastapi import APIRouter, HTTPException, status
from models.user import UserIn
from database import database, user_table
from security import get_user

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserIn):
    if await get_user(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with that email already exists"
        )
    # TODO: store hashed password
    query = user_table.insert().values(email=user.email, password=user.password)

    await database.execute(query)
    return {"details": "User created."}

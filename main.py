from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers.post import router as post_router
from routers.user import router as user_router
from database import database


# functiono that setup and finish the process when "yield" finish
@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)

app.include_router(post_router)
app.include_router(user_router)

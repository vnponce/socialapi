from fastapi import FastAPI
from routers.post import router as post_routers

app = FastAPI()

app.include_router(post_routers)

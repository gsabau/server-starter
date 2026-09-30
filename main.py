from fastapi import FastAPI

from user_repository import UserRepository
from user_router import build_router
from user_service import UserService

app = FastAPI()
repository = UserRepository()
service = UserService(repository)
app.include_router(build_router(service))

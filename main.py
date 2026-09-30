from fastapi import FastAPI

from message_repository import MessageRepository
from message_router import build_router
from message_service import MessageService

app = FastAPI()
repository = MessageRepository()
service = MessageService(repository)
app.include_router(build_router(service))

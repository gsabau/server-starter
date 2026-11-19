import logging

from app.computer_chat.chat_agent import create_chat_agent
from app.computer_chat.router import build_router as build_computer_chat_router
from app.computer_chat.service import ComputerChatService
from app.computer_moves.game_agent import create_game_agent
from app.computer_moves.router import build_router as build_computer_move_router
from app.computer_moves.service import ComputerMoveService
from app.fixtures import load_fixtures
from app.game_histories.repository import GameHistoryRepository
from app.game_histories.router import build_router as build_history_router
from app.game_histories.service import GameHistoryService
from app.profiles.repository import ProfileRepository
from app.profiles.router import build_router as build_profile_router
from app.profiles.service import ProfileService
from app.users.repository import UserRepository
from app.users.router import build_router as build_user_router
from app.users.service import UserService
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()  # reads .env once, before anything reads the environment

# uvicorn configures its own loggers, not these ones.
# One handler here, so agent calls show up and other libraries stay quiet.
for _logger_name in ("app.computer_moves", "app.computer_chat"):
    _agent_logger = logging.getLogger(_logger_name)
    _agent_logger.setLevel(logging.INFO)
    if not _agent_logger.handlers:
        _handler = logging.StreamHandler()
        _handler.setFormatter(logging.Formatter("%(levelname)s %(name)s: %(message)s"))
        _agent_logger.addHandler(_handler)
    _agent_logger.propagate = False

app = FastAPI(title="Tic Tac Toe API", description="API for Tic Tac Toe game", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

users = UserRepository()
profiles = ProfileRepository()
histories = GameHistoryRepository()

user_service = UserService(users)
profile_service = ProfileService(profiles, users)
history_service = GameHistoryService(histories)
computer_move_service = ComputerMoveService(create_game_agent())
computer_chat_service = ComputerChatService(
    create_chat_agent(), user_service, profile_service, history_service
)

app.include_router(build_user_router(user_service))
app.include_router(build_profile_router(profile_service))
app.include_router(build_history_router(history_service))
app.include_router(build_computer_move_router(computer_move_service))
app.include_router(build_computer_chat_router(computer_chat_service))

load_fixtures(user_service, profile_service, history_service)

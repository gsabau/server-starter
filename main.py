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
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

app.include_router(build_user_router(user_service))
app.include_router(build_profile_router(profile_service))
app.include_router(build_history_router(history_service))

load_fixtures(user_service, profile_service, history_service)

from fastapi import FastAPI

from app.games.repository import GameRepository
from app.games.router import build_router as build_game_router
from app.games.service import GameService
from app.profiles.repository import ProfileRepository
from app.profiles.router import build_router as build_profile_router
from app.profiles.service import ProfileService
from app.scores.repository import ScoreRepository
from app.scores.router import build_router as build_score_router
from app.scores.service import ScoreService
from app.users.repository import UserRepository
from app.users.router import build_router as build_user_router
from app.users.service import UserService

app = FastAPI()

users = UserRepository()
profiles = ProfileRepository()
games = GameRepository()
scores = ScoreRepository()

user_service = UserService(users)
profile_service = ProfileService(profiles, users)
score_service = ScoreService(scores)
game_service = GameService(games, users, scores)

app.include_router(build_user_router(user_service))
app.include_router(build_profile_router(profile_service))
app.include_router(build_game_router(game_service))
app.include_router(build_score_router(score_service))

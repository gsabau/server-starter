from fastapi import APIRouter, HTTPException

from app.domain.models import Game
from app.games.service import GameNotFoundError, GameService, IllegalMoveError, SameUserError, UnknownUserError
from app.schemas import GameCreate, GameResponse, MoveCreate


def build_router(service: GameService) -> APIRouter:
    router = APIRouter(prefix="/games", tags=["games"])

    @router.post("", status_code=201)
    def create_game(body: GameCreate) -> GameResponse:
        return _to_response(_run(lambda: service.create_game(body.player_x_user_id, body.player_o_user_id)))

    @router.get("")
    def list_games() -> list[GameResponse]:
        return [_to_response(game) for game in service.list_games()]

    @router.get("/{game_id}")
    def get_game(game_id: int) -> GameResponse:
        return _to_response(_run(lambda: service.get_game(game_id)))

    @router.post("/{game_id}/moves")
    def move(game_id: int, body: MoveCreate) -> GameResponse:
        return _to_response(_run(lambda: service.move(game_id, body.cell)))

    return router


def _run(action):
    try:
        return action()
    except UnknownUserError:
        raise HTTPException(status_code=404, detail="User not found")
    except SameUserError:
        raise HTTPException(status_code=400, detail="Users must differ")
    except GameNotFoundError:
        raise HTTPException(status_code=404, detail="Game not found")
    except IllegalMoveError as error:
        raise HTTPException(status_code=400, detail=error.detail)


def _to_response(game: Game) -> GameResponse:
    return GameResponse(
        id=game.id,
        board=list(game.board),
        next=game.next,
        status=game.status,
        player_x_user_id=game.player_x_user_id,
        player_o_user_id=game.player_o_user_id,
    )

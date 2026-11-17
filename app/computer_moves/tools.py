from dataclasses import dataclass

from pydantic_ai import RunContext  # pyright: ignore[reportMissingImports]

# The function calls of the agent. This is the file you extend.
#
# The model never sees the Python code. It only sees a schema built from three things:
#   1. the function name,
#   2. the parameters (name, type),
#   3. the docstring (what the function is for, and what each parameter means).
# From that schema alone the model decides whether to call the function and with which values.
# So: the name says what it does (verb + object), the docstring says what it is for and
# when to use it, not how it is done.
#
# A new function call = one function here + one entry in TOOLS below.
# A plain "def" is enough. Use "async def" only if the function itself waits for something
# slow (an HTTP request, a database).


# pydantic-ai calls the data that is handed to the tools "deps" (dependencies).
# Here it is the game context of one computer turn: the board and the mark go in,
# the move comes out. The model never sees it.
@dataclass
class GameContext:
    board: list[str]  # nine cells, "" (empty), "X" or "O"
    mark: str  # the mark of the computer
    move: int | None = None  # the position the computer played, None until a move was accepted


def place_computer_mark(ctx: RunContext[GameContext], position: int) -> str:
    """Place the computer's mark on one free cell of the board. Use this to make the computer's move.

    position: the cell, a whole number from 0 to 8. 0 to 2 is the top row, 3 to 5 the middle row, 6 to 8 the bottom row.
    """
    game_context = ctx.deps
    free = [index for index, cell in enumerate(game_context.board) if cell == ""]
    if position not in free:
        return f"Position {position} is not free. Free positions: {', '.join(str(index) for index in free)}."
    game_context.move = position
    return f"Placed {game_context.mark} at position {position}."


TOOLS = [place_computer_mark]

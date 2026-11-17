import os

from pydantic_ai import Agent
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider

from app.computer_moves.tools import TOOLS, GameContext

# The agent context. Who the agent is, and what it may delegate.
# Keep it short: a small model skips tool calls when the rules get long.
# The board and the mark are not here, they come with every request (see service.py).
SYSTEM_PROMPT = """You are a Tic-Tac-Toe player. You play one mark, X or O.
You cannot move by writing text. You act only through your tools.
To make your move, call the move tool once with a free position.
If a tool reports an error, choose another position and call it again.
"""


def create_game_agent() -> Agent[GameContext, str]:
    # MODEL_NAME, MODEL_BASE_URL and MODEL_API_KEY come from the environment.
    # main.py loads the .env file once at startup. Without it the defaults below apply.
    model = OllamaModel(
        os.environ.get("MODEL_NAME", "llama3.2"),
        provider=OllamaProvider(
            base_url=os.environ.get("MODEL_BASE_URL", "http://127.0.0.1:11434/v1"),
            api_key=os.environ.get("MODEL_API_KEY", "ollama"),
        ),
    )

    return Agent(
        model,
        deps_type=GameContext,
        system_prompt=SYSTEM_PROMPT,
        tools=TOOLS,
        model_settings={"temperature": 0.0},
    )

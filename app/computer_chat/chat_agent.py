import os

from pydantic_ai import Agent
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider

from app.computer_chat.tools import TOOLS, ChatContext

# Keep it short: a small model skips tool calls when the rules get long.
SYSTEM_PROMPT = """You are the Tic-Tac-Toe game assistant.
Answer questions about Tic-Tac-Toe, players, profiles, games, and high scores.
When a question needs stored data (such as users, profiles, games, or high scores), call a tool first and answer only from its result.
Keep answers short and answer in the language of the question.
"""


def create_chat_agent() -> Agent[ChatContext, str]:
    model = OllamaModel(
        os.environ.get("MODEL_NAME", "llama3.2"),
        provider=OllamaProvider(
            base_url=os.environ.get("MODEL_BASE_URL", "http://127.0.0.1:11434/v1"),
            api_key=os.environ.get("MODEL_API_KEY", "ollama"),
        ),
    )

    return Agent(
        model,
        deps_type=ChatContext,
        system_prompt=SYSTEM_PROMPT,
        tools=TOOLS,
        model_settings={"temperature": 0.0},
    )

from message import Message
from message_repository import MessageRepository


class MessageNotFoundError(Exception):
    pass


class EmptyMessageError(Exception):
    pass


class MessageService:
    """Logic layer. Knows the rules. Does not know HTTP."""

    def __init__(self, repository: MessageRepository):
        self._repository = repository

    def list_messages(self) -> list[Message]:
        return self._repository.list_all()

    def get_message(self, message_id: int) -> Message:
        message = self._repository.get(message_id)
        if message is None:
            raise MessageNotFoundError
        return message

    def create_message(self, text: str) -> Message:
        self._require_text(text)
        return self._repository.add(text)

    def update_message(self, message_id: int, text: str) -> Message:
        self._require_text(text)
        message = self._repository.replace(message_id, text)
        if message is None:
            raise MessageNotFoundError
        return message

    def delete_message(self, message_id: int) -> None:
        if not self._repository.remove(message_id):
            raise MessageNotFoundError

    def _require_text(self, text: str) -> None:
        if not text.strip():
            raise EmptyMessageError

from message import Message


class MessageRepository:
    """Data layer. The dict stands in for the database."""

    def __init__(self):
        self._messages = {1: Message(id=1, text="hello")}
        self._next_id = 2

    def list_all(self) -> list[Message]:
        return list(self._messages.values())

    def get(self, message_id: int) -> Message | None:
        return self._messages.get(message_id)

    def add(self, text: str) -> Message:
        message = Message(id=self._next_id, text=text)
        self._messages[message.id] = message
        self._next_id += 1
        return message

    def replace(self, message_id: int, text: str) -> Message | None:
        current = self._messages.get(message_id)
        if current is None:
            return None
        current.text = text
        return current

    def remove(self, message_id: int) -> bool:
        if message_id not in self._messages:
            return False
        del self._messages[message_id]
        return True

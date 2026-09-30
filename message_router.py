from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from message import Message
from message_service import EmptyMessageError, MessageNotFoundError, MessageService


class MessageBody(BaseModel):
    text: str


class MessageResponse(BaseModel):
    id: int
    text: str


def build_router(service: MessageService) -> APIRouter:
    """Presentation layer. Routes only. Calls the service."""

    router = APIRouter(prefix="/messages", tags=["messages"])

    @router.get("")
    def list_messages() -> list[MessageResponse]:
        return [_to_response(message) for message in service.list_messages()]

    @router.get("/{message_id}")
    def get_message(message_id: int) -> MessageResponse:
        return _to_response(_run(lambda: service.get_message(message_id)))

    @router.post("", status_code=201)
    def create_message(body: MessageBody) -> MessageResponse:
        return _to_response(_run(lambda: service.create_message(body.text)))

    @router.put("/{message_id}")
    def update_message(message_id: int, body: MessageBody) -> MessageResponse:
        return _to_response(_run(lambda: service.update_message(message_id, body.text)))

    @router.delete("/{message_id}", status_code=204)
    def delete_message(message_id: int) -> None:
        _run(lambda: service.delete_message(message_id))

    return router


def _run(action):
    try:
        return action()
    except MessageNotFoundError:
        raise HTTPException(status_code=404, detail="Message not found")
    except EmptyMessageError:
        raise HTTPException(status_code=400, detail="Text is empty")


# Message and MessageResponse have the same two fields. The mapping is the
# boundary between the app and the HTTP response, not a change of data.
# Message is the dataclass the repository and the service pass around. Those
# layers do not know JSON. MessageResponse is the Pydantic model FastAPI turns
# into JSON and into the OpenAPI page. This function is the only place that
# copies id and text. MessageBody is already a different shape: only text,
# because the client does not send the id. The response mapping is the same
# idea in the other direction. A later field on Message that should stay inside
# the server is left out here.
def _to_response(message: Message) -> MessageResponse:
    return MessageResponse(id=message.id, text=message.text)

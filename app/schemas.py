from dataclasses import dataclass
from typing import Annotated, Literal

from pydantic import Field


# Request and response shapes. A dataclass, fields only.
# The stored rows live in app/domain/models.py.
# Every field carries Annotated[..., Field(description=..., examples=[...])].
# FastAPI copies the text into /openapi.json and shows it on /docs.
# The class docstring becomes the description of the whole schema.
# A cell is "", "X", or "O". A game is nine cells, index 0 to 8, row by row.


@dataclass
class UserCreate:
    """Body für einen neuen Account. Die `id` schickt der Client nicht, sie vergibt der Server."""

    name: Annotated[
        str,
        Field(
            description="Name des neuen Accounts. Pflicht. Ein leerer Name oder nur Leerzeichen ist ungültig (400). Leerzeichen am Rand werden entfernt.",
            examples=["Ada"],
        ),
    ]


@dataclass
class UserResponse:
    """Ein Account, wie ihn der Server zurückgibt."""

    id: Annotated[
        int,
        Field(
            description="Eindeutige Id des Accounts. Vergibt der Server, die erste Id ist 1. Im Profil heißt sie `user_id`.",
            examples=[1],
        ),
    ]
    name: Annotated[
        str,
        Field(
            description="Name des Accounts, ohne Leerzeichen am Rand.",
            examples=["Ada"],
        ),
    ]


@dataclass
class ProfileCreate:
    """Body für ein neues Profil. Ein Profil ist der öffentliche Anzeigename eines Accounts."""

    user_id: Annotated[
        int,
        Field(
            description="Id eines vorhandenen Accounts (`id` aus `/users`). Unbekannte Id: 404. Pro Account gibt es genau ein Profil, ein zweites ist ungültig (400).",
            examples=[1],
        ),
    ]
    display_name: Annotated[
        str,
        Field(
            description="Name, den die App am Sitzplatz anzeigt. Muss nicht dem Account-Namen entsprechen.",
            examples=["Ada"],
        ),
    ]
    bio: Annotated[
        str,
        Field(
            description="Kurzer Text zum Account. Darf leer sein.",
            examples=["Spielt gerne."],
        ),
    ]
    hobbies: Annotated[
        list[str],
        Field(
            description="Hobbys als Liste von Texten. Darf leer sein.",
            examples=[["Schach"]],
        ),
    ]


@dataclass
class ProfileResponse:
    """Ein Profil, wie es der Server zurückgibt."""

    id: Annotated[
        int,
        Field(
            description="Eindeutige Id des Profils. Vergibt der Server.",
            examples=[1],
        ),
    ]
    user_id: Annotated[
        int,
        Field(
            description="Id des Accounts, zu dem das Profil gehört (`id` aus `/users`).",
            examples=[1],
        ),
    ]
    display_name: Annotated[
        str,
        Field(
            description="Name, den die App am Sitzplatz anzeigt.",
            examples=["Ada"],
        ),
    ]
    bio: Annotated[
        str,
        Field(
            description="Kurzer Text zum Account. Darf leer sein.",
            examples=["Spielt gerne."],
        ),
    ]
    hobbies: Annotated[
        list[str],
        Field(
            description="Hobbys als Liste von Texten. Darf leer sein.",
            examples=[["Schach"]],
        ),
    ]


@dataclass
class GameHistoryCreate:
    """Body für ein fertiges Spiel. Die App spielt selbst und meldet nur das Ergebnis. Die `id` schickt der Client nicht, sie vergibt der Server."""

    player_a: Annotated[
        str,
        Field(
            description="Name der Person, die X spielt und beginnt. Nicht leer und verschieden von `player_b` (sonst 400). Leerzeichen am Rand werden entfernt.",
            examples=["Ada"],
        ),
    ]
    player_b: Annotated[
        str,
        Field(
            description="Name der Person, die O spielt. Nicht leer und verschieden von `player_a` (sonst 400). Leerzeichen am Rand werden entfernt.",
            examples=["Cleo"],
        ),
    ]
    game: Annotated[
        list[str],
        Field(
            description='Das ganze Brett am Ende des Spiels, genau neun Felder, Zeile für Zeile: Index 0 bis 2 ist die erste Zeile, 3 bis 5 die zweite, 6 bis 8 die dritte. Ein Feld ist "" (leer), "X" oder "O". Andere Länge oder anderer Wert: 400.',
            examples=[["X", "O", "O", "", "X", "", "", "", "X"]],
        ),
    ]
    winner: Annotated[
        str,
        Field(
            description='Name des Siegers. Genau `player_a` oder `player_b`. Bei einem Unentschieden der Text "draw". Alles andere: 400.',
            examples=["Ada"],
        ),
    ]


@dataclass
class GameHistoryResponse:
    """Ein fertiges Spiel, wie es der Server gespeichert hat."""

    id: Annotated[
        str,
        Field(
            description='Eindeutige Id des Eintrags als Text, zum Beispiel "1". Vergibt der Server. Sie steht im Pfad `/game-histories/{history_id}`.',
            examples=["1"],
        ),
    ]
    player_a: Annotated[
        str,
        Field(
            description="Name der Person, die X gespielt hat und begann.",
            examples=["Ada"],
        ),
    ]
    player_b: Annotated[
        str,
        Field(
            description="Name der Person, die O gespielt hat.",
            examples=["Cleo"],
        ),
    ]
    game: Annotated[
        list[str],
        Field(
            description='Das Brett am Ende, genau neun Felder, Zeile für Zeile (Index 0 bis 2 erste Zeile, 3 bis 5 zweite, 6 bis 8 dritte). Ein Feld ist "" (leer), "X" oder "O".',
            examples=[["X", "O", "O", "", "X", "", "", "", "X"]],
        ),
    ]
    winner: Annotated[
        str,
        Field(
            description='Name des Siegers (`player_a` oder `player_b`) oder "draw" bei einem Unentschieden.',
            examples=["Ada"],
        ),
    ]


@dataclass
class ComputerMoveRequest:
    """Anfrage nach dem nächsten Zug des Computers. Das Brett ist der aktuelle Stand, mitten im Spiel. Der Server speichert nichts."""

    game: Annotated[
        list[str],
        Field(
            description='Das aktuelle Brett, genau neun Felder, Zeile für Zeile: Index 0 bis 2 ist die erste Zeile, 3 bis 5 die zweite, 6 bis 8 die dritte. Ein Feld ist "" (leer), "X" oder "O".',
            examples=[["X", "O", "", "", "X", "", "", "", "O"]],
        ),
    ]
    mark: Annotated[
        Literal["X", "O"],
        Field(
            description='Das Zeichen des Computers, "X" oder "O". Der Computer setzt dieses Zeichen auf ein freies Feld.',
            examples=["O"],
        ),
    ]


@dataclass
class ComputerMoveResponse:
    """Der Zug, den der Computer gewählt hat. Die App setzt das Zeichen selbst auf dieses Feld."""

    position: Annotated[
        int,
        Field(
            description="Das gewählte Feld, eine ganze Zahl von 0 bis 8, Zeile für Zeile. Das Feld ist im geschickten Brett frei.",
            examples=[2],
        ),
    ]


@dataclass
class ComputerChatRequest:
    """Frage oder Nachricht an den Chat-Agenten rund um das Spiel. Der Server speichert nichts."""

    text: Annotated[
        str,
        Field(
            description="Frage oder Text an den Chat-Agenten, zum Beispiel zu Spielregeln, Spielern, Profilen oder Highscores.",
            examples=["Welche Spieler gibt es?"],
        ),
    ]


@dataclass
class ComputerChatResponse:
    """Antwort des Chat-Agenten als Text."""

    reply: Annotated[
        str,
        Field(
            description="Antwort des Chat-Agenten auf die gestellte Frage.",
            examples=["Aktuell sind Ada, Ben, Cleo und Dan registriert."],
        ),
    ]


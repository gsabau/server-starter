# Server-Starter

Zwei Module. FastAPI ist die Anwendung. Uvicorn ist der Prozess, der auf dem Port wartet. Eines ohne das andere reicht nicht: `python main.py` legt nur das App-Objekt an und beendet sich.

## Drei Schichten

Jede Schicht kennt nur die nächste darunter. `main.py` verbindet sie.

| Schicht | Name | Datei | Aufgabe |
|---|---|---|---|
| Daten | `MessageRepository` | `message_repository.py` | Liest und schreibt. Das Dict ist die Datenbank. Start: eine Nachricht `hello`. |
| Logik | `MessageService` | `message_service.py` | Holt die Daten über das Repository. Leerer Text ist ungültig. Fehlende Id ist ein Fehler. Kennt kein HTTP. |
| Präsentation | `build_router` | `message_router.py` | Die FastAPI-Routen. Fragt den Service. Macht aus dem Ergebnis JSON und aus dem Fehler einen Status. |

`Message` in `message.py` ist das Objekt, das die Schichten weitergeben: `id` und `text`.

Methoden der Daten: `list_all`, `get`, `add`, `replace`, `remove`.

Methoden der Logik: `list_messages`, `get_message`, `create_message`, `update_message`, `delete_message`.

Routen:

- `GET /messages`
- `GET /messages/{message_id}`
- `POST /messages` mit `{"text": "..."}`
- `PUT /messages/{message_id}` mit `{"text": "..."}`
- `DELETE /messages/{message_id}`

## FastAPI

FastAPI ist das Python-Modul für die HTTP-Anwendung. In `main.py` steht `app = FastAPI()`. Die Routen stehen in `message_router.py`. Eine Route ist eine URL plus eine Funktion. `@router.get("/messages")` heißt: bei `GET /messages` die Liste holen.

Die Funktion gibt ein Modell zurück. FastAPI macht daraus JSON. Die erste Nachricht ist `{"id": 1, "text": "hello"}`.

FastAPI schreibt die OpenAPI-Beschreibung selbst: Pfad, Methode, JSON. Das ist keine zweite Datei zum Bearbeiten. Die Seite dafür ist `/docs`. Das Schema liegt unter `/openapi.json`.

Damit bleibt die Beschreibung an der Route. Eine neue Route erscheint in `/docs`, sobald der Server sie geladen hat.

## Uvicorn

Uvicorn ist das Programm, das Verbindungen annimmt. FastAPI öffnet keinen Port. Uvicorn lädt `app` aus `main.py` und reicht jede Anfrage dorthin.

```powershell
uvicorn main:app --reload
```

`main` ist die Datei `main.py`. `app` ist die Variable `app = FastAPI()`. `--reload` startet neu, wenn du die Datei speicherst. Der Server hört auf `http://127.0.0.1:8000`.

Das Terminal bleibt offen und zeigt den Start. **Strg+C** beendet den Prozess. Danach antwortet der Port nicht mehr.

## Einrichten

Alles in diesem Ordner. Einmalig.

`python main.py` startet den Server nicht. Die Datei legt nur die Anwendung an und ist sofort fertig. Die Eingabezeile kommt zurück. Es läuft nichts.

Zuerst die Umgebung und die Pakete. `uvicorn` gibt es erst danach. Ohne Installation meldet PowerShell, dass der Befehl `uvicorn` unbekannt ist.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Nach `Activate.ps1` steht `(.venv)` vor der Eingabezeile. Das ist das Python, in dem `uvicorn` liegt.

## Server starten

```powershell
uvicorn main:app --reload
```

Der Server läuft, wenn das Terminal offen bleibt und `Uvicorn running on http://127.0.0.1:8000` zeigt. Die Eingabezeile kommt nicht zurück.

Die Liste: [http://127.0.0.1:8000/messages](http://127.0.0.1:8000/messages). Dort steht die Nachricht `hello`.

Die Beschreibung: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Server stoppen

Im selben Terminal **Strg+C**. Die Eingabezeile kommt zurück. Die beiden Adressen antworten nicht mehr.

## Lizenz

MIT. Siehe [LICENSE.md](LICENSE.md).

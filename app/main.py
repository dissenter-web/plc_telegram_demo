from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import BOT_TOKEN, BOT_USERNAME, DATA_FILE
from app.storage import Storage
from app.telegram_api import send_message


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

storage = Storage(DATA_FILE)


EVENTS = {
    "stop": "Остановить конвейер",
    "start": "Запустить конвейер",
    "call": "Вызвать наладчика",
    "alarm": "Авария 1",
    "reset": "Сброс аварии",
}


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "bot_username": BOT_USERNAME,
            "events": storage.get_events()[::-1],
        },
    )


@app.post("/api/events")
async def create_event(data: dict):
    event_type = data.get("event_type")

    if not event_type or event_type not in EVENTS:
        raise HTTPException(status_code=400, detail="Unknown event")

    label = EVENTS[event_type]
    event = storage.add_event(event_type, label)

    chat_id = storage.get_active_chat()

    if chat_id:
        try:
            await send_message(
                BOT_TOKEN,
                chat_id,
                f"{label}\n{event['created_at']}",
            )
        except Exception as e:
            # не валим API из-за Telegram
            print(f"Telegram error: {e}")

    return {"ok": True, "event": event}


@app.get("/api/events")
async def get_events():
    return storage.get_events()[::-1]
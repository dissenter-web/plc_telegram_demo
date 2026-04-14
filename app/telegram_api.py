import httpx


async def send_message(token: str, chat_id: int | str, text: str):
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(
            url,
            json={
                "chat_id": chat_id,
                "text": text
            }
        )

    # проверка HTTP статуса
    response.raise_for_status()

    data = response.json()

    # проверка ответа Telegram
    if not data.get("ok"):
        raise Exception(f"Telegram API error: {data}")

    return data
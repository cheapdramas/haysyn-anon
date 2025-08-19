import asyncio
import websockets
import json

from core.auth import create_jwt
from core.config import WEBSOCKET_URL

ws_tasks: dict[str, asyncio.Task] = {}


async def websocket_client(user_id: str, message):
    token = create_jwt("bot") 
    url = f"{WEBSOCKET_URL}?token={token}&admin_id={user_id}"

    try:
        async with websockets.connect(url) as websocket:
            print("✅ Connected to server")

            try:
                while True:
                    msg = await websocket.recv()
                    if msg != []:
                        for post in json.loads(msg):
                            await message.answer(post["text"])

            except websockets.exceptions.ConnectionClosed as e:
                print("❌ Connection closed:", e)

            except asyncio.CancelledError:
                print(f"🛑 WebSocket client for {user_id} cancelled")
                await websocket.close()
                raise  # <- щоб коректно завершилась таска

            except Exception as e:
                print("⚠️ Unexpected error:", e)
                await websocket.close()

    except Exception as e:
        print(f"❌ Could not connect WebSocket for {user_id}: {e}")
        await message.answer("🚫 Не вдалось підключитися до сервера")

    finally:
        await message.answer("Закрито з'єднання з вебсокетом")
        ws_tasks.pop(user_id, None)

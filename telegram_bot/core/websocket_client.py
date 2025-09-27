import asyncio
import websockets
import json
from core.auth import create_jwt
from core.config import WEBSOCKET_URL
from websockets import WebSocketClientProtocol
from core.messages import mod_message
from keyboards.inline import keyboard_mod
from dataclasses import dataclass
from schemas.post import PostModStatus , WSPostModerate

from db.mod_messages_crud import ModMessagesCrud 

@dataclass
class WsEntry:
    task: asyncio.Task
    ws: WebSocketClientProtocol

ws_tasks: dict[str, WsEntry] = {}


async def websocket_client(user_id: str, message):
    token = create_jwt("bot") 
    url = f"{WEBSOCKET_URL}?token={token}&admin_id={user_id}"

    try:
        async with websockets.connect(url) as websocket:
            print("✅ Connected to server")
            ws_tasks.get(user_id)["ws"] = websocket

            try:
                while True:
                    msg = await websocket.recv() 
                    if msg != []: 
                        for post in json.loads(msg):
                            msg = mod_message(post)
                            keyboard = keyboard_mod(post["id"])
                            msg_sent = await message.answer(msg,reply_markup=keyboard, parse_mode="HTML")
                            # add message to list of messages that waits for mod
                            ModMessagesCrud.add(
                                message_id=msg_sent.message_id,
                                admin_id=user_id,
                                post_id=post["id"]
                            )




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

async def manage_post(user_id: str, post_id: str, status: PostModStatus):
    if not ws_tasks.get(user_id):
        print("decline_post: Websocket is not created")
        return
    websocket = ws_tasks.get(user_id)["ws"]

    post_mod_info = WSPostModerate(post_id=post_id,status=status)
    post_mod_info_dict = {"post_id":post_mod_info.post_id,"status":post_mod_info.status.value}

    try:
        await websocket.send(json.dumps(post_mod_info_dict))
    except Exception as e:
        print("manage_post ERROR:", str(e))
        await websocket.close()
        ws_tasks.pop(user_id)

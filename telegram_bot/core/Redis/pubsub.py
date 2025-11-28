from re import A
from core.Redis.client import get_redis
from core.Redis.scripts import get_post, remove_unprocessed_post
from core.channel import send_message_to_channel
from core.config import CHANNEL_ID, REDIS_CHANNEL_NAME, ADMINS, WEBSITE_URL_BASE
from core.messages import mod_message
from keyboards.inline import keyboard_link, keyboard_mod
from db.crud import ChanellMessagesCrud, ModMessagesCrud
from core.api_communication import get_post as api_get_post


# code that works in the background and sends post to admin in telegram
async def listen_to_redis(bot):
    r = await get_redis()
    pubsub = r.pubsub()
    await pubsub.subscribe(REDIS_CHANNEL_NAME)

    print("Listening to Redis ...")
    
    try: 
        async for message in pubsub.listen():
            print("Pubsub got data from channel: ", message)
            if message["type"] == "message":
                msg_text = message["data"]
                #got a new post
                if msg_text.startswith("new_post:"):
                    post_id = msg_text.split(":")[1]

                    post_data = await get_post("post:" + post_id)

                    msg = mod_message(post_data)
                    keyboard = keyboard_mod(post_id)

                    for admin_id in ADMINS:
                        try:
                            msg_sent = await bot.send_message(
                                text=msg,
                                chat_id=admin_id,
                                reply_markup=keyboard,
                                parse_mode="HTML"
                            )
                            await ModMessagesCrud.add(
                                message_id=msg_sent.message_id,
                                admin_id=admin_id,
                                post_id=post_id
                            )
                            # remove post_id from unprocessed_posts
                            await remove_unprocessed_post("post:" + post_id)
                        except Exception as e:
                            print(f"Failed to send mod message to admin_id: {admin_id}", str(e))
                if msg_text.startswith("to_tg_channel:"):
                    post_id = msg_text.split(":")[1]
                    if await ChanellMessagesCrud.get(post_id=post_id) == []:
                        try:
                            print("POST_ID:", post_id)



                            # make a request to api to get post data
                            post_data = await api_get_post(post_id)
                            if not post_data:
                                return

                            msg = mod_message(post_data) 
                            keyboard = keyboard_link(text="Посилання на пост",url=f"{WEBSITE_URL_BASE}post/{post_id}")
                            await send_message_to_channel(post_id ,post_data.get("telegram_user_id"), bot, msg, keyboard)

                        except Exception as e:

                            print(f"Failed to send post to telegram channel (listen_to_redis): ", str(e))

    except Exception as e:
        print(f"Error in listen_to_redis: ",str(e))

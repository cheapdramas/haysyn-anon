from re import A
from core.Redis.client import get_redis
from core.Redis.scripts import RawPost, UnprocessedPosts, RawPost
from core.channel import send_message_to_channel, send_post_to_channel
from core.config import CHANNEL_ID, REDIS_CHANNEL_NAME, ADMINS, WEBSITE_URL_BASE
from core.messages import message_post_format
from keyboards.inline import keyboard_link, keyboard_mod
from db.crud import ChanellMessagesCrud, ModMessagesCrud
from core.api_communication import api_get_post, api_set_post_in_tg_channel


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

                    post_data = await RawPost.get("post:" + post_id)

                    msg = message_post_format(post_data)
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
                            await UnprocessedPosts.remove("post:" + post_id)

                        except Exception as e:
                            print(f"Failed to send mod message to admin_id: {admin_id}", str(e))
                if msg_text.startswith("to_tg_channel:"):
                    post_id = msg_text.split(":")[1]
                    await send_post_to_channel(post_id, bot)
                    

    except Exception as e:
        print(f"Error in listen_to_redis: ",str(e))







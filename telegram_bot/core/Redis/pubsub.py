from core.Redis.client import get_redis
from core.Redis.scripts import get_post, remove_unprocessed_post
from core.config import REDIS_CHANNEL_NAME, ADMINS
from core.messages import mod_message
from keyboards.inline import keyboard_mod
from db.mod_messages_crud import ModMessagesCrud



async def listen_to_redis(bot):
    r = await get_redis()
    pubsub = r.pubsub()
    await pubsub.subscribe(REDIS_CHANNEL_NAME)

    print("Listening to Redis ...")
    
    try: 
        async for message in pubsub.listen():
            print("Pubsub got data from channel: ", message)
            if message["type"] == "message":
                #got a new post
                post_id = message["data"]

                post_data = await get_post("post:" + post_id)

                msg = mod_message(post_data)
                keyboard = keyboard_mod(post_id)

                for admin_id in ADMINS:
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
        print(f"Error in listen_to_redis: ",str(e))

from aiogram import Bot
from aiogram.types import Message
from core.api_communication import get_posts
from keyboards.inline import keyboard_link, keyboard_webapp, keyboard_continue_viewing_posts
from core.config import CHANNEL_ID, WEBSITE_URL_BASE, MAX_POSTS_AMOUNT_TO_USER
from db.crud import ChanellMessagesCrud
from core.auth import  anonymize_user_id
from core.messages import mod_message


async def send_posts_from_website(
    message: Message,
    offset: int,
    limit: int,
    exclude: list[int] | list,
    in_tg_channel: bool | None = None
) -> int:
    """
        Selects posts from user that are still on website,
        and send <limit> of them to user chat.
        Returns whether were sent <limit> of posts or were not
    """

    anon_user_id = anonymize_user_id(str(message.chat.id))
    website_posts = await get_posts(
        anon_user_id,
        offset=offset,
        limit=limit,
        exclude=[],
        in_tg_channel=in_tg_channel
    )

    for post in website_posts:
        msg = mod_message(post)
        await message.answer(text=msg, parse_mode="HTML", reply_markup=keyboard_link(text="Посилання на пост",url=f"{WEBSITE_URL_BASE}post/{post['id']}"))

    return len(website_posts)

async def send_posts_from_channel(
    message: Message, 
    bot: Bot, 
    offset: int = 0, 
    limit: int = 5, 
    user_id: int | None = None,
) -> int:
    """
        Selects posts from user that were sent to telegram channel,
        and send <limit> of them to user chat.
        Returns amount of sent posts   
    """
    userId = message.from_user.id
    if user_id:
        userId = user_id

    
    anon_user_id = anonymize_user_id(str(message.chat.id))
    sent_posts = 0 
    channel_posts = []

    while sent_posts < limit: # to send <limit> of existing in telegram channel posts
        channel_posts = await ChanellMessagesCrud.get(
            user_id=anon_user_id, 
            start = offset, 
            amount = limit
        )
        print(channel_posts)

        if channel_posts == []:
            break

        for post in channel_posts:
            try:
                await bot.forward_message(
                    chat_id=userId,
                    from_chat_id=CHANNEL_ID,
                    message_id=post.message_id
                )
                sent_posts += 1 

            except Exception as e:
                print(f"Message {post.message_id} forward failed for user: {message.from_user.id}", str(e))

        offset = offset + len(channel_posts) 

    return sent_posts



async def myposts(message: Message, bot: Bot, offset: int, limit: int = MAX_POSTS_AMOUNT_TO_USER, load_from_website: bool = False, user_id: int | None = None) -> None:
    if load_from_website:
        website_send_posts = await send_posts_from_website(message, offset, limit, [], in_tg_channel=False)

        if website_send_posts == limit:
            await message.answer(text = "Продовжити дивитись пости?", reply_markup=keyboard_continue_viewing_posts(limit + offset, get_from_channel=False))
        else:
            await message.answer(text="❌ Кінець твоїх постів")

        return 

    sent_posts_channel = await send_posts_from_channel(message, bot, offset, limit, user_id)
    print(sent_posts_channel)

    if sent_posts_channel < limit:
        sent_posts_website = await send_posts_from_website(message, 0, limit - sent_posts_channel, [], in_tg_channel=False) 

        if sent_posts_channel + sent_posts_website == limit:
            await message.answer(text = "Продовжити дивитись пости?", reply_markup=keyboard_continue_viewing_posts(sent_posts_website, get_from_channel=False))
        else:
            await message.answer(text="❌ Кінець твоїх постів")

    else:
        await message.answer(text = "Продовжити дивитись пости?", reply_markup=keyboard_continue_viewing_posts(limit + offset, get_from_channel=True))



        




# async def myposts_command(message: Message, bot: Bot, offset: int = 0, limit: int = 5, get_from_website: bool = False):
#     user_id = message.chat.id
#     anon_user_id = anonymize_user_id(str(user_id))
#
#     if get_from_website:
#         website_posts = await send_posts_from_website_to_user(
#             message=message,
#             anon_user_id=anon_user_id,
#             offset=offset,
#             limit=limit,
#             exclude=[]
#         )
#         print(website_posts)
#
#         if len(website_posts) == limit:
#             await message.answer(text = "Продовжити дивитись пости?", reply_markup=keyboard_continue_viewing_posts(limit + offset, get_from_channel=False))
#         else:
#             await message.answer("❌ Кінець постів ❌")
#
#         return
#
#
#
#
#
#     sent_posts = []
#
#     while len(sent_posts) < limit:
#         channel_posts = await ChanellMessagesCrud.get(
#             user_id=anon_user_id, 
#             start = offset, 
#             amount = limit
#         )
#
#         if channel_posts == []:
#             break
#
#         for post in channel_posts:
#             try:
#                 await bot.forward_message(
#                     chat_id=message.from_user.id,
#                     from_chat_id=CHANNEL_ID,
#                     message_id=post.message_id
#                 )
#                 sent_posts.append(post.post_id)
#
#             except:
#                 print(f"Message {post.message_id} forward failed for user: {anon_user_id}")
#
#         offset = limit - len(sent_posts) + 1
#
#     # if posts from channel are over, but we still need to send 5 posts
#     if len(sent_posts) < limit:
#         website_posts = await send_posts_from_website_to_user(
#             message=message,
#             anon_user_id=anon_user_id,
#             offset=0,
#             limit=limit - len(sent_posts),
#             exclude=sent_posts
#         )
#
#         if len(sent_posts) + len(website_posts) == limit:
#             await message.answer(text = "Продовжити дивитись пости?", reply_markup=keyboard_continue_viewing_posts(limit, get_from_channel=False))
#
#     else:
#         await message.answer(text = "Продовжити дивитись пости?", reply_markup=keyboard_continue_viewing_posts(limit + offset, get_from_channel=True))
#
#
#
#
#
# # async def forward_user_posts_from_channel(message: Message , bot: Bot, start: int = 0, amount: int = 10, last_post_index:int = 0) -> None:
# #     user_id = message.chat.id
# #     anon_user_id = anonymize_user_id(str(user_id))
# #     print(f"/myposts triggered from user: {user_id}")
# #
# #     posts_channel = await ChanellMessagesCrud.get(anon_user_id, start=start, amount = amount)
# #     print("posts from channel: ", posts_channel, "anon_user_id: ", anon_user_id, "user_id: ", str(user_id))
# #     # або немає постів в каналі взагалі, або ми зайшли в цю функцію повторно, і пости закінчились (last_post_index > 0)
# #     if posts_channel == []:
# #         posts_api = await get_posts_by_tg_user_id(str(user_id)) # ALL posts from user
# #         print("posts_api: ", posts_api)
# #             # get all chanell posts from user for comparison
# #
# #         if posts_api == []:
# #             await message.answer(text="❌Ти ще не написав жодного посту❌\n\n⬇",reply_markup=keyboard_webapp(text="Написати пост",url=WEBSITE_URL_BASE))
# #             return
# #         for post in posts_api:
# #             if not await ChanellMessagesCrud.get(post_id=post['id'], start=None, amount = None):
# #                 msg = mod_message(post)
# #                 await message.answer(text=msg, reply_markup=keyboard_link(text="Посилання на пост",url=f"{WEBSITE_URL_BASE}post/{post['id']}"), parse_mode="HTML")
# #
# #         await message.answer(text="❌ Кінець твоїх постів ")
# #
# #
# #     else: # пости з <start> для цього юзера в каналі існують
# #         try:    
# #             #forward posts from channel to user
# #             await bot.forward_messages(
# #                 chat_id=message.from_user.id,
# #                 from_chat_id=CHANNEL_ID,
# #                 message_ids=[i.message_id for i in posts_channel]
# #             )
# #
# #             #send message to continue viewing posts
# #             await bot.send_message(
# #                 chat_id=user_id,
# #                 text="Продовжити дивитись пости?",
# #                 reply_markup=keyboard_continue_viewing_posts(last_post_index + len(posts_channel))
# #             )
# #
# #         except Exception as e:
# #             print(f"Post forwarding failed for {user_id}", type(e))

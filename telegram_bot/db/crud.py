from sqlalchemy.future import select
from .utils import db_helper
from .models import ModMessages, ChanellMessages
from typing import Sequence

class ModMessagesCrud:
    @staticmethod
    async def add(
        message_id: int,
        admin_id: int,
        post_id: str
    ) -> ModMessages:
        try:
            async with db_helper.session_factory() as session:
                message_info = ModMessages(
                    message_id = message_id,
                    admin_id = admin_id,
                    post_id = post_id
                )
                session.add(message_info)
                await session.commit()
                await session.refresh(message_info)
                return message_info
        except Exception as e:
            print("Error occured! ModMessagesCrud.add : ",str(e))

    @staticmethod
    async def get(post_id: str) -> Sequence[ModMessages]:
        try:
            async with db_helper.session_factory() as session:
                q = select(ModMessages).filter(ModMessages.post_id == post_id)

                result = await session.execute(q)
                return result.scalars().all()
        except Exception as e:
            print(f"Error occured! ModMessagesCrud.get with post_id: {post_id}: ",str(e))

    @staticmethod
    async def delete(post_id:str) -> bool:
        try:
            async with db_helper.session_factory() as session:
                q = (
                    select(ModMessages)
                    .filter(
                        ModMessages.post_id == post_id
                    )
                )
                posts = await session.execute(q)

                for post in posts.scalars():
                    await session.delete(post)
                await session.commit()
                return True
        except Exception as e:
            print(f"Error occured! ModMessagesCrud.delete with post_id: {post_id}: ",str(e))
            return False


class ChanellMessagesCrud:
    @staticmethod
    async def add(
        user_id: str,
        message_id: str
    ) -> ChanellMessages:
        try:
            async with db_helper.session_factory() as session:
                message_info = ChanellMessages(
                    user_id=user_id,
                    message_id=message_id
                )
                session.add(message_info)
                await session.commit()
                await session.refresh(message_info)
                return message_info
        except Exception as e:
            print("Error occured! ChanellMessages.add : ",str(e))

    @staticmethod
    async def get(
        user_id: str,
        start: int = 0,
        amount: int = 20
    ) -> Sequence[ChanellMessages]:
        try:
            async with db_helper.session_factory() as session:
                q = select(ChanellMessages).filter(ChanellMessages.user_id==user_id).offset(start).limit(amount)
                result = await session.execute(q)
                return result.scalars().all()        
        except Exception as e:
            print("Error occured! ChanellMessages.add : ",str(e))






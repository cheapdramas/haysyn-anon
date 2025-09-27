from .utils import db_helper
from .models import ModMessages 


class ModMessagesCrud:
    @staticmethod
    def add(
        message_id: int,
        admin_id: int,
        post_id: str
    ) -> ModMessages:
        try:
            with db_helper.session_factory() as session:
                message_info = ModMessages(
                    message_id = message_id,
                    admin_id = admin_id,
                    post_id = post_id
                )
                session.add(message_info)
                session.commit()
                return message_info
        except Exception as e:
            print("Error occured while adding mod message to db: ",str(e))

    @staticmethod
    def get(post_id: str) -> list[ModMessages]:
        try:
            with db_helper.session_factory() as session:
                return session.query(ModMessages).filter(ModMessages.post_id == post_id).all()

        except Exception as e:
            print(f"Error occured while getting mod message with post_id: {post_id}: ",str(e))

    @staticmethod
    def delete(post_id:str):
        try:
            with db_helper.session_factory() as session:
                (
                    session.query(ModMessages)
                    .filter(
                        ModMessages.post_id == post_id
                    )
                    .delete(synchronize_session=False)
                )
                session.commit()
                return True
        except Exception as e:
            print(f"Error occured while getting mod message with post_id: {post_id}: ",str(e))



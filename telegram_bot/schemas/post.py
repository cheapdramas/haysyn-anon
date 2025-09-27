from pydantic import BaseModel
from enum import Enum

class PostModStatus(Enum):
    approved = "approved"
    declined = "declined"
class WSPostModerate(BaseModel):
    post_id: str
    status: PostModStatus

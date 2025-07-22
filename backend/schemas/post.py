from pydantic import BaseModel, StringConstraints
from typing import Annotated 
from config import PostConfig

class PostBase(BaseModel):
	title: Annotated[str, StringConstraints(max_length=PostConfig.max_title_len)]
	text: str

class PostCreate(PostBase):
	pass

class PostRead(PostBase):
	id: int
from pydantic import BaseModel

class PostBase(BaseModel):
	text: str

class PostCreate(PostBase):
	pass

class PostRead(PostBase):
	id: int
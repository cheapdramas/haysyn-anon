from pydantic import BaseModel, StringConstraints
from typing import Annotated 
from dataclasses import dataclass

@dataclass
class PostConfig:
    max_title_len: int = 40
    max_text_len: int = 2200 

class Post(BaseModel):
    title: Annotated[str, StringConstraints(max_length=PostConfig.max_title_len)]
    text: Annotated[str, StringConstraints(max_length=PostConfig.max_text_len)]

class PostSend(Post):
    id: str



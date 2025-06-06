from pydantic import BaseModel
from typing import Optional

class CommentIn(BaseModel):
    comment: str
    published: str  # "true", "false", or "check"
    reason: str
    username: Optional[str] = "user"
    timestamp: Optional[str] = None

class CommentOut(BaseModel):
    _id: str
    comment: str
    published: str
    reason: str
    username: Optional[str] = "user"
    timestamp: Optional[str] = None

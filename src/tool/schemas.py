from pydantic import BaseModel
from typing import Optional

class ToolBase(BaseModel):
    name: str
    description: str|None
    cityid: int
    userid: int

class ToolSelect(ToolBase):
    id: int

    class Config:
        from_attributes = True

class ToolUpdate(ToolBase):
    name: Optional[str]
    description: Optional[str|None]
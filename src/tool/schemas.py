from pydantic import BaseModel

class ToolBase(BaseModel):
    name: str
    description: str|None
    cityid: int
    userid: int

class ToolSelect(ToolBase):
    id: int

    class Config:
        # from_attributes = True
        orm_mode = True
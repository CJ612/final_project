from fastapi import HTTPException, status
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Tool
from database.models import User


class CRUDTool:

    @staticmethod
    async def get(session: AsyncSession, tool_id: int):
        tool = select(Tool).filter(Tool.id == tool_id)
        tool = await session.execute(tool)
        tool = tool.scalar_one()
        return tool


    @staticmethod
    async def get_all(session: AsyncSession):
        tools = await session.execute(select(Tool))
        tools = tools.scalars().all()
        return tools

    @staticmethod
    async def create(session: AsyncSession, tool_data: dict):
        tool = Tool(**tool_data)
        session.add(tool)
        await session.commit()
        await session.refresh(tool)
        return tool

    @staticmethod
    async def update(session: AsyncSession, tool: Tool, tool_data: dict):
        for key, value in tool_data.items():
            setattr(tool, key, value)
        await session.commit()
        await session.refresh(tool)
        return tool

    @staticmethod
    async def delete(session: AsyncSession, tool: Tool):
        await session.delete(tool)
        await session.commit()


    @staticmethod
    async def get_tool_by_toolname_and_userid(session: AsyncSession, toolname: str, user_id: int):
        tool = select(Tool).filter(Tool.name == toolname, Tool.userid == user_id)
        tool = await session.execute(tool)
        tool = tool.scalar_one_or_none()
        
        return tool
    
    @staticmethod
    async def get_all_by_user_id(session: AsyncSession, user_id: int):
        tools = await session.execute(select(Tool).filter(Tool.userid == user_id))
        tools = tools.scalars().all()
        
        return tools
    
    @staticmethod
    async def get_tool_by_toolid_and_userid(session: AsyncSession, tool_id: str, user_id: int):
        tool = select(Tool).filter(Tool.id == tool_id, Tool.userid == user_id)
        tool = await session.execute(tool)
        tool = tool.scalar_one_or_none()
        
        return tool
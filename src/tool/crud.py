from fastapi import HTTPException, status
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Tool


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
    async def get_tool_by_toolname(session: AsyncSession, toolname: str):
        tool = select(Tool).filter(Tool.name == toolname)
        tool = await session.execute(tool)
        tool = tool.scalar_one_or_none()
        if tool is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Tool not found"
            )
        return tool
    
    @staticmethod
    async def get_all_by_user_id(session: AsyncSession, user_id: int):
        tools = await session.execute(select(Tool).filter(Tool.userid == user_id))
        tools = tools.scalars().all()
        if tools is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Tools not found"
            )
        return tools
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_session
from tool.crud import CRUDTool
from sqlalchemy.exc import NoResultFound


async def get_tool(tool_id: int, session: AsyncSession = Depends(get_session)):
    try:
        tool = await CRUDTool.get(session, tool_id)
        return tool
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tool not found"
        )
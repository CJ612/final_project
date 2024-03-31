from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_session
from database.models import Tool, User
from tool.schemas import ToolBase, ToolSelect
from tool.crud import CRUDTool
from measurement.crud import CRUDMeasurement
from tool.dependency import get_tool
from user.router import get_current_user



router = APIRouter(
    prefix="/tool",
    tags=["tool"],
)

@router.get("/{tool_id}", response_model=ToolSelect)
async def read_tool(tool: Tool = Depends(get_tool), user: User = Depends(get_current_user)):
    return tool

@router.post("/", response_model=ToolBase)
async def create_tool(tool: ToolBase, session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    tool = await CRUDTool.create(session, tool.dict())
    return tool


@router.put("/{tool_id}", response_model=ToolSelect)
async def update_tool(
    tool_create: ToolBase,
    tool: Tool = Depends(get_tool),
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    tool = await CRUDTool.update(session, tool, tool_create.dict())
    return tool


@router.delete("/{tool_id}")
async def delete_tool(
    tool: Tool = Depends(get_tool), session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user),
):
    # обновить на None все measurements 
    measurements = await CRUDMeasurement.get_all_by_tool(session, tool.id)
    for measurement in measurements:
        measurement.dict()["toolid"] = None
        measurement = await CRUDMeasurement.update(session, measurement, measurement.dict())
    tool = await CRUDTool.delete(session, tool)
    return status.HTTP_204_NO_CONTENT
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.config import settings
from api.api_v1.schemas.tea_make import TeaMakeCreate, TeaMakeResponse
from core.models import db_helper, Tea_make
from crud.tea_make import make_tea, get_tea, post_tea_ready, get_tea_ready

router = APIRouter(
   prefix=settings.api.prefix,
   tags=["Tea_make"]
)

@router.post("/tea-make", response_model=dict)
async def post_tea_make(
       tea_make: TeaMakeCreate,
       session: AsyncSession = Depends(db_helper.session_getter)
):
   tea_make = await  make_tea(session=session, tea_data=tea_make)
   return {"status": "success", "order_id": tea_make.id}


@router.get("/tea-make/{device_id}", response_model=TeaMakeResponse)
async def get_tea_make(
       device_id: str,
       session: AsyncSession = Depends(db_helper.session_getter)):
   tea_make = await get_tea(session=session, device_id=device_id)
   if not tea_make:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No order")
   return tea_make


@router.post("/tea-make/{order_id}/complete", response_model=dict)
async def tea_make_ready(
       order_id: int,
       session: AsyncSession = Depends(db_helper.session_getter)
):
   tea_make = await post_tea_ready(session=session, order_id=order_id)
   if not tea_make:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
   if tea_make.status != 'completed':
       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Order not in progress")
   return {"status": "completed", "order_id": tea_make.id}


@router.get("/tea-make/{order_id}/status", response_model=dict)
async def get_order_status(
    order_id: int,
    session: AsyncSession = Depends(db_helper.session_getter)
):
    order = await get_tea_ready(session=session, order_id=order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return {"status": order.status, "order_id": order.id}


@router.delete("/tea-make")
async def clear_all_orders(session: AsyncSession = Depends(db_helper.session_getter)):
    try:
        await session.execute(text("DELETE FROM tea_make"))
        await session.commit()
        return {"message": "Deleted tea orders"}
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


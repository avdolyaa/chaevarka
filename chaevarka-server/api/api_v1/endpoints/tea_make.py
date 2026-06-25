from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from datetime import datetime
from api.dependencies.authentication.auth import current_active_user, current_superuser
from core.config import settings
from api.api_v1.schemas.tea_make import TeaMakeCreate, TeaMakeResponse, TeaStatusUpdate, TeaStatus
from core.models import db_helper, Tea_make, Device, User
from crud.tea_make import make_tea, get_tea, get_tea_ready, update_tea_status, cancel_tea_order, dispense_tea
from sqlalchemy import select


router = APIRouter(
   prefix=settings.api.prefix,
   tags=["Tea_make"]
)

async def check_device_access(
    session: AsyncSession,
    device_id: str,
    user_id: int
) -> None:
    user = await session.get(User, user_id)
    if not user or user.device_id != device_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this device"
        )


async def update_device_online(session: AsyncSession, device_id: str):
    device = await session.scalar(
        select(Device).where(Device.device_id == device_id)
    )

    if device:
        device.online_at = datetime.utcnow()
        session.add(device)

@router.post("/tea-make", response_model=dict)
async def post_tea_make(
        tea_make: TeaMakeCreate,
        current_user=Depends(current_active_user),
        session: AsyncSession = Depends(db_helper.session_getter)
):
    await check_device_access(session, tea_make.device_id, current_user.id)
    result = await make_tea(session=session, tea_data=tea_make)
    return {"status": "success", "order_id": result.id}


@router.get("/tea-make/{device_id}", response_model=TeaMakeResponse)
async def get_tea_make(
       device_id: str,
       session: AsyncSession = Depends(db_helper.session_getter)):
   tea_make = await get_tea(session=session, device_id=device_id)
   if not tea_make:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No order")
   await update_device_online(session, device_id)
   await session.commit()
   return tea_make


@router.post("/tea-make/{order_id}/complete", response_model=dict)
async def tea_make_ready(
        order_id: int,
        session: AsyncSession = Depends(db_helper.session_getter)
):
    tea_make = await session.get(Tea_make, order_id)
    if not tea_make:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    if tea_make.status in ('completed', 'cancelled', 'waiting'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Order not in progress")
    tea_make.status = 'completed'
    session.add(tea_make)
    await session.commit()
    await session.refresh(tea_make)

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


@router.delete("/tea-make", dependencies=[Depends(current_superuser)])
async def clear_all_orders(session: AsyncSession = Depends(db_helper.session_getter)):
    try:
        await session.execute(text("DELETE FROM tea_make"))
        await session.commit()
        return {"message": "Deleted tea orders"}
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.patch("/tea-make/{order_id}/status", response_model=dict)
async def update_order_status(
        order_id: int,
        status_data: TeaStatusUpdate,
        session: AsyncSession = Depends(db_helper.session_getter)
):
    order = await update_tea_status(
        session=session,
        order_id=order_id,
        new_status=status_data.status
    )
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    return {
        "status": "success",
        "order_id": order.id,
        "new_status": order.status,
        "message": f"Order status updated to {order.status}"
    }


@router.get("/tea-make/order/{order_id}", response_model=TeaMakeResponse)
async def get_order_by_id(
    order_id: int,
    session: AsyncSession = Depends(db_helper.session_getter)
):
    order = await session.get(Tea_make, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.post("/tea-make/{order_id}/cancel", response_model=dict)
async def cancel_tea(
        order_id: int,
        current_user=Depends(current_active_user),
        session: AsyncSession = Depends(db_helper.session_getter)
):
    order = await session.get(Tea_make, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    await check_device_access(session, order.device_id, current_user.id)
    try:
        order = await cancel_tea_order(session=session, order_id=order_id)

        return {
            "status": "success",
            "order_id": order.id,
            "message": f"Order cancelled. Status is now {order.status}"
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/tea-make/{order_id}/dispense", response_model=dict)
async def dispense_tea_portion(
        order_id: int,
        session: AsyncSession = Depends(db_helper.session_getter),
        current_user=Depends(current_active_user)
):
    order = await session.get(Tea_make, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    await check_device_access(session, order.device_id, current_user.id)
    result = await dispense_tea(session=session, order_id=order_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Order not found")
    if result == "wrong_status":
        raise HTTPException(
            status_code=400,
            detail="Cannot dispense. Order is not ready (need: ready_to_dispense)"
        )
    return {
        "status": "success",
        "order_id": result.id,
        "message": f"Command sent: pour {result.water_for_cup}ml"
    }

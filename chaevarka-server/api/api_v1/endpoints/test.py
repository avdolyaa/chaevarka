from fastapi import APIRouter, Depends
from core.config import settings
from core.models import db_helper, Device, Tea_make
import random
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

router = APIRouter(
    prefix=settings.api.prefix,
    tags=["Test"]
)

@router.post("/test-data")
async def test_data(session: AsyncSession = Depends(db_helper.session_getter)):
    try:
        devices = [
            Device(device_id="chvrk_1", ip_address="192.168.1.100"),
            Device(device_id="chvrk_2", ip_address="192.168.1.101"),
            Device(device_id="chvrk_3", ip_address="192.168.1.101"),
        ]
        for device in devices:
            session.add(device)

        for i in range(10):
            order = Tea_make(
                device_id=random.choice(["chvrk_1", "chvrk_2", "chvrk_3"]),
                water=random.randint(50, 300),
                temperature=random.randint(70, 100),
                sugar=random.randint(0, 5),
                type=random.randint(0, 6),
                time=random.randint(0, 5),
                tea_cnt=random.randint(1, 10),
                status=random.choice(["waiting", "in_progress", "completed"]),
                created_at=datetime.utcnow() - timedelta(hours=random.randint(1, 24))
            )
            session.add(order)

        await session.commit()

        return {"message": "Added 3 devices and 10 orders"}

    except Exception as e:
        await session.rollback()
        return {"error": str(e)}

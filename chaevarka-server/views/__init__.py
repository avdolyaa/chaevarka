from fastapi import APIRouter
from views.verification import router as verification_router
from views.reset_password import router as reset_password_router
router = APIRouter()
router.include_router(verification_router)
router.include_router(reset_password_router)
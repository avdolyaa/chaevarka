from typing import Annotated

from fastapi import APIRouter, Request, Depends, HTTPException, Form
from api.dependencies.authentication import get_user_manager
from jinja_templates import templates

router = APIRouter(
    prefix="/reset-password",
)



@router.get(
    "/",
    include_in_schema=False,
    name="reset-password",
)
async def reset_password_page(
    request: Request,
    token: str,
):
    return templates.TemplateResponse(
        "reset_password.html",
        {"request": request, "token": token}
    )

@router.post(
    "/",
    include_in_schema=False,
)
async def reset_password_action(
    request: Request,
    token: Annotated[str, Form()],
    password: Annotated[str, Form()],
    user_manager=Depends(get_user_manager)
):
    try:
        await user_manager.reset_password(token, password, request)
        return templates.TemplateResponse(
            "after_reset_password.html",
            {"request": request, "success": True, "message": "Пароль успешно изменен!"}
        )
    except Exception:
        return templates.TemplateResponse(
            "after_reset_password.html",
            {"request": request, "success": False, "message": "Ошибка: ссылка устарела."}
        )
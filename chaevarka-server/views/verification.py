from fastapi import APIRouter, Request, Depends, HTTPException
from api.dependencies.authentication import get_user_manager
from jinja_templates import templates

router = APIRouter(
    prefix="/verify-email",
)


@router.get(
    "/",
    include_in_schema=False,
    name="verify-email",
)
async def verify_email_page(
    request: Request,
    token: str,
    user_manager=Depends(get_user_manager),
):
    try:
        user = await user_manager.verify(token)

        return templates.TemplateResponse(
            "verification.html",
            {
                "request": request,
                "user": user,
                "success": True
            },
        )
    except Exception:
        return templates.TemplateResponse(
            "verification.html",
            {
                "request": request,
                "success": False
            }
        )
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.schemas.recipe import RecipeResponse, RecipeCreate, RecipePatch
from api.dependencies.authentication.auth import current_active_user
from core.config import settings
from core.models import db_helper, Recipe
from crud.recipe import get_all_public_recipes, get_my_recipes, crud_delete_recipe, crud_create_recipe, update_recipe

router = APIRouter(
   prefix=settings.api.prefix,
   tags=["Tea_make"],
)


@router.get("/", response_model=List[RecipeResponse])
async def read_public_recipes(
        session: AsyncSession = Depends(db_helper.session_getter)
):
    recipes = await get_all_public_recipes(session=session)
    return recipes


@router.get("/my", response_model=List[RecipeResponse])
async def read_my_recipes(
        current_user=Depends(current_active_user),
        session: AsyncSession = Depends(db_helper.session_getter)
):
    recipes = await get_my_recipes(session=session, user_id=current_user.id)
    return recipes


@router.post("/", response_model=RecipeResponse)
async def create_recipe(
        recipe_in: RecipeCreate,
        current_user=Depends(current_active_user),
        session: AsyncSession = Depends(db_helper.session_getter)
):
    recipe = await crud_create_recipe(session, recipe_in, user_id=current_user.id)
    return recipe


@router.delete("/{recipe_id}")
async def delete_recipe(
        recipe_id: int,
        current_user=Depends(current_active_user),
        session: AsyncSession = Depends(db_helper.session_getter)
):
    recipe = await session.get(Recipe, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="The recipe wasn't found")
    if recipe.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your recipe")

    await crud_delete_recipe(session=session, recipe=recipe)
    return {"ok": True}




@router.patch("/{recipe_id}", response_model=RecipeResponse)
async def patch_recipe(
        recipe_id: int,
        recipe_update: RecipePatch,
        current_user=Depends(current_active_user),
        session: AsyncSession = Depends(db_helper.session_getter)
):
    recipe = await session.get(Recipe, recipe_id)

    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    if recipe.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only edit your own recipes")

    return await update_recipe(session=session, recipe=recipe, recipe_update=recipe_update)
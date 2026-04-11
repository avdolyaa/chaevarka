from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.schemas.recipe import RecipeCreate, RecipePatch
from core.models import Recipe


async def get_all_public_recipes(session: AsyncSession) -> list[Recipe]:
    stmt = select(Recipe).where(Recipe.is_public == True).order_by(Recipe.id)
    result = await session.execute(stmt)
    return list(result.scalars().all())

async def get_my_recipes(session: AsyncSession, user_id: int) -> list[Recipe]:
    stmt = select(Recipe).where(Recipe.user_id == user_id).order_by(Recipe.id)
    result = await session.execute(stmt)
    return list(result.scalars().all())

async def crud_create_recipe(session: AsyncSession, recipe_in: RecipeCreate, user_id: int) -> Recipe:
    db_recipe = Recipe(**recipe_in.model_dump(), user_id=user_id)
    session.add(db_recipe)
    await session.commit()
    await session.refresh(db_recipe)
    return db_recipe

async def crud_delete_recipe(session: AsyncSession, recipe: Recipe) -> None:
    await session.delete(recipe)
    await session.commit()



async def update_recipe(session: AsyncSession, recipe: Recipe, recipe_update: RecipePatch
) -> Recipe:

    update_data = recipe_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(recipe, key, value)

    await session.commit()
    await session.refresh(recipe)
    return recipe
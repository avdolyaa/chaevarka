from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from typing import Annotated

class RecipeBase(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None
    type: str = "black"
    icon: Optional[str] = None

    waterAmount: Annotated[int, Field(ge=50, le=2000, alias="water_amount")]
    temperature: Annotated[int, Field(ge=70, le=100)]
    time: Annotated[int, Field(ge=0, le=5)]
    teaAmount: Annotated[int, Field(ge=0, le=10, alias="tea_amount")]

    drum1: int = Field(default=0, alias="drum_1")
    drum2: int = Field(default=0, alias="drum_2")
    drum3: int = Field(default=0, alias="drum_3")
    drum4: int = Field(default=0, alias="drum_4")
    drum5: int = Field(default=0, alias="drum_5")
    drum6: int = Field(default=0, alias="drum_6")

    isPublic: bool = Field(default=False, alias="is_public")


class RecipeCreate(RecipeBase):
    pass


class RecipePatch(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    title: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    icon: Optional[str] = None

    waterAmount: Optional[Annotated[int, Field(ge=100, le=1000)]] = Field(None, alias="water_amount")
    temperature: Optional[Annotated[int, Field(ge=70, le=100)]] = None
    time: Optional[Annotated[int, Field(ge=0, le=5)]] = None
    teaAmount: Optional[Annotated[int, Field(ge=0, le=10)]] = Field(None, alias="tea_amount")

    drum1: Optional[int] = Field(None, ge=0, le=100, alias="drum_1")
    drum2: Optional[int] = Field(None, ge=0, le=100, alias="drum_2")
    drum3: Optional[int] = Field(None, ge=0, le=100, alias="drum_3")
    drum4: Optional[int] = Field(None, ge=0, le=100, alias="drum_4")
    drum5: Optional[int] = Field(None, ge=0, le=100, alias="drum_5")
    drum6: Optional[int] = Field(None, ge=0, le=100, alias="drum_6")

    isPublic: Optional[bool] = Field(None, alias="is_public")


class RecipeResponse(RecipeBase):
    id: int
    userId: int = Field(alias="user_id")
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
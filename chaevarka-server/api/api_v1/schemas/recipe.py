from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from typing import Annotated

class RecipeBase(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None
    type: str = "black"
    icon: Optional[str] = None

    water_amount: Annotated[int, Field(ge=50, le=2000, alias="waterAmount")]
    temperature: Annotated[int, Field(ge=70, le=100)]
    time: Annotated[int, Field(ge=0, le=5)]
    tea_amount: Annotated[int, Field(ge=0, le=10, alias="teaAmount")]

    drum_1: int = Field(default=0, alias="drum1")
    drum_2: int = Field(default=0, alias="drum2")
    drum_3: int = Field(default=0, alias="drum3")
    drum_4: int = Field(default=0, alias="drum4")
    drum_5: int = Field(default=0, alias="drum5")
    drum_6: int = Field(default=0, alias="drum6")

    is_public: bool = Field(default=False, alias="isPublic")


class RecipeCreate(RecipeBase):
    pass


class RecipePatch(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    title: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    icon: Optional[str] = None

    water_amount: Optional[Annotated[int, Field(ge=100, le=1000)]] = Field(None,  alias="waterAmount")
    temperature: Optional[Annotated[int, Field(ge=70, le=100)]] = None
    time: Optional[Annotated[int, Field(ge=0, le=5)]] = None
    tea_amount: Optional[Annotated[int, Field(ge=0, le=10)]] = Field(None, alias="teaAmount")

    drum_1: Optional[int] = Field(None, ge=0, le=100, alias="drum1")
    drum_2: Optional[int] = Field(None, ge=0, le=100, alias="drum2")
    drum_3: Optional[int] = Field(None, ge=0, le=100, alias="drum3")
    drum_4: Optional[int] = Field(None, ge=0, le=100, alias="drum4")
    drum_5: Optional[int] = Field(None, ge=0, le=100, alias="drum5")
    drum_6: Optional[int] = Field(None, ge=0, le=100, alias="drumv6")

    isPublic: Optional[bool] = Field(None, alias="is_public")


class RecipeResponse(RecipeBase):
    id: int
    user_id: int = Field(alias="userId")
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
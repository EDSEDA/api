from pydantic import BaseModel, Field

from typing import List

from .enums import SexEnum
from .enums import RaceEnum
from .enums import EmotionEnum


class CreateUserRecommendationMessage(BaseModel):
    cash_register_id: int = Field(description='ID кассы', example='123')
    embedding: List[float] = Field(description='Эмбеддинг юзера', example='[0.0, 0.0, 0.0]')
    user_id: int = Field(description='ID юзера', example='123')
    age: int = Field(description='Возраст', example='12')
    sex: SexEnum = Field(description='Пол', example='M')
    race: RaceEnum = Field(description='Раса', example='European')
    emotion: EmotionEnum = Field(description='Текущая эмоция', example='Happy')

from pydantic import BaseModel, Field

from .enums import SexEnum
from .enums import RaceEnum
from .enums import EmotionEnum


class CreateUserRecommendationMessage(BaseModel):
    cash_register_id: int = Field(description='ID кассы', example=123)
    user_id: int = Field(description='ID юзера', example=123)
    age: int = Field(description='Возраст', example=123)
    sex: SexEnum = Field(description='Пол', example='male')
    race: RaceEnum = Field(description='Раса', example='white')
    emotion: EmotionEnum = Field(description='Текущая эмоция', example='neutral')


class UserRecommendationMessage(BaseModel):
    cash_register_id: int = Field(description='ID кассы', example=123)
    user_id: int = Field(description='ID юзера', example=123)
    recommendations: list[int] = Field(description='Айдишники рекомендованных товаров', example=[1, 2, 3, 4, 5])

from pydantic import BaseModel, Field

from typing import List

from grifon.video_analysis.enums import SexEnum
from grifon.video_analysis.enums import RaceEnum
from grifon.video_analysis.enums import EmotionEnum

class VideoAnalysMessage(BaseModel):
    cash_register_id: int = Field(description='Описание', example='Пример')
    embedding: List[float] = Field(description='Описание', example='Пример')
    person_id: int = Field(description='Описание', example='Пример')
    age: int = Field(description='Описание', example='Пример')
    sex: SexEnum = Field(description='Описание', example='Пример')
    race: RaceEnum = Field(description='Описание', example='Пример')
    emotion: EmotionEnum = Field(description='Описание', example='Пример')


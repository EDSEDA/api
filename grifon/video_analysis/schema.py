from typing import List

from pydantic import Field
from faust import Record

from grifon.video_analysis.enums import EmotionEnum
from grifon.video_analysis.enums import RaceEnum
from grifon.video_analysis.enums import SexEnum


class VideoAnalyseMessage(Record, serializer='json'):
    cash_register_id: int = Field(description='Описание', example='Пример')
    embedding: List[float] = Field(description='Описание', example='Пример')
    person_id: int = Field(description='Описание', example='Пример')
    age: int = Field(description='Описание', example='Пример')
    sex: SexEnum = Field(description='Описание', example='Пример')
    race: RaceEnum = Field(description='Описание', example='Пример')
    emotion: EmotionEnum = Field(description='Описание', example='Пример')


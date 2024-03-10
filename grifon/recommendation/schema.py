from pydantic import BaseModel, Field

from .enums import ExampleEnum


class ExampleClass(BaseModel):
    field1: str = Field(description='Описание', example='Пример')
    field2: str | None = Field(description='Описание', example='Пример')
    field3: ExampleEnum = ExampleEnum.field3

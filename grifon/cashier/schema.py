from pydantic import BaseModel, Field


class RequestUpdateMessage(BaseModel):
    cash_register_id: int = Field(description='ID кассы', example=123)


class AddItemAndRequestUpdateMessage(BaseModel):
    cash_register_id: int = Field(description='ID кассы', example=123)
    itemId: int = Field(description='ID товара', example=123)

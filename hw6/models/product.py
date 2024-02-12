# Таблица товаров должна содержать следующие поля:
# id (PRIMARY KEY), название, описание и цена.

from pydantic import BaseModel, Field


class ProductIn(BaseModel):
    title: str = Field(..., title='title', max_length=120)
    description: str = Field(default='', title='description', max_length=300)
    price: float = Field(..., title='price', gt=0, le=10_000)


class Product(ProductIn):
    prod_id: int
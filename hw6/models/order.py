# Таблица заказов должна содержать следующие поля:
# id (PRIMARY KEY), id пользователя (FOREIGN KEY), id товара (FOREIGN KEY), дата заказа и статус заказа.
import datetime
from enum import Enum
from pydantic import BaseModel, Field, EmailStr


class Status(Enum):
    placed = 'размещен',
    unpaid = 'ожидает оплаты'
    paid = 'оплачен'
    shipped = 'отправлен'
    delivering = 'доставляется'
    delivered = 'доставлен'
    completed = 'выполнен'
    cancelled = 'отменен'


class OrderIn(BaseModel):
    user_id: int = Field(..., title='user_id')
    prod_id: int = Field(..., title='prod_id')
    date: datetime.date = Field(..., title='date')
    status: Status = Field(..., title='status')

    class Config:
        use_enum_values = True


class Order(OrderIn):
    order_id: int
    firstname: str
    lastname: str
    email: EmailStr
    title: str
    description: str
    price: float
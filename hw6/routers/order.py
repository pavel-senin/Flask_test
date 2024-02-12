from typing import List
from sqlalchemy import select
from fastapi import APIRouter
from ex_06.db import users, products, orders, database
from ex_06.models.order import Order, OrderIn

router = APIRouter()


@router.post("/orders/", response_model=Order)
async def create_order(order: OrderIn):
    """Создание заказа в БД, create"""
    query = orders.insert().values(user_id=order.user_id, prod_id=order.product_id,
                                   date=order.date, status=order.status)
    last_record_id = await database.execute(query)
    return {**order.dict(), "order_id": last_record_id}


@router.get("/orders/", response_model=List[Order])
async def read_orders():
    """Чтение заказов из БД, read"""
    query = select(orders.c.id.label('order_id'), orders.c.date.label('date'),
                   orders.c.status.label('status'),
                   users.c.id.label('user_id'), users.c.first_name.label('firstname'),
                   users.c.last_name.label('lastname'), users.c.email.label('email'),
                   products.c.id.label('prod_id'), products.c.title.label('title'),
                   products.c.description.label('description'), products.c.price.label('price')
                   ).join(products).join(users)
    return await database.fetch_all(query)


@router.get("/orders/{order_id}", response_model=Order)
async def read_order(order_id: int):
    """Чтение одного заказа из БД, read"""
    query = select(orders.c.id.label('order_id'), orders.c.date.label('date'),
                   orders.c.status.label('status'),
                   users.c.id.label('user_id'), users.c.first_name.label('firstname'),
                   users.c.last_name.label('lastname'), users.c.email.label('email'),
                   products.c.id.label('prod_id'), products.c.title.label('title'),
                   products.c.description.label('description'), products.c.price.label('price')
                   ).join(products).join(users)
    return await database.fetch_one(query)


@router.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: int, new_order: OrderIn):
    """Обновление заказа в БД, update"""
    query = orders.update().where(orders.c.order_id == order_id).values(**new_order.dict())
    await database.execute(query)
    return {**new_order.dict(), "order_id": order_id}


@router.delete("/orders/{order_id}")
async def delete_user(order_id: int):
    """Удаление заказа из БД, delete"""
    query = orders.delete().where(orders.c.order_id == order_id)
    await database.execute(query)
    return {'message': 'Order deleted'}
import datetime
from random import randint, choice
from fastapi import APIRouter
from ex_06.db import users, products, orders, database

router = APIRouter()
# MIN_NUM = 10
# MAX_NUM = 100
MIN_PRICE = 1
MAX_PRICE = 10_000


@router.get("/fake_data/")
async def create_note(user_count: int, prod_count: int, order_count: int):
    """Добавление тестовых пользователей в БД"""
    for i in range(user_count):
        query = users.insert().values(firstname=f'firstname_{i}',
                                      lastname=f'lastname_{i}',
                                      email=f'mail{i}@m.t',
                                      password=f'password{i}')
        await database.execute(query)

    """Добавление тестовых товаров в БД"""
    for i in range(prod_count):
        query = products.insert().values(title=f'title_{i}',
                                         description=f'description_{i}',
                                         price=randint(MIN_PRICE, MAX_PRICE))
        await database.execute(query)

    """Добавление тестовых заказов в БД"""
    for i in range(order_count):
        query = orders.insert().values(user_id=randint(1, user_count),
                                       prod_id=randint(1, prod_count),
                                       date=datetime.date.today(),
                                       status=choice(['размещен', 'ожидает оплаты', 'оплачен', 'отправлен',
                                                      'доставляется', 'доставлен', 'выполнен', 'отменен']))
        await database.execute(query)

    return {'message': f'{user_count} fake users, {prod_count} fake products'
                       f'and {order_count} fake orders created'}
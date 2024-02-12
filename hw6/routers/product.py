from typing import List

from fastapi import APIRouter
from ex_06.db import users, products, database
from ex_06.models.product import Product, ProductIn

router = APIRouter()


@router.post("/products/", response_model=Product)
async def create_prod(product: ProductIn):
    """Создание товара в БД, create"""
    query = products.insert().values(title=product.title, description=product.description, price=product.price)
    last_record_id = await database.execute(query)
    return {**product.dict(), "prod_id": last_record_id}


@router.get("/products/", response_model=List[Product])
async def read_prods():
    """Чтение товаров из БД, read"""
    query = products.select()
    return await database.fetch_all(query)


@router.get("/product/{prod_id}", response_model=Product)
async def read_prod(prod_id: int):
    """Чтение одного товара из БД, read"""
    query = products.select().where(products.c.user_id == prod_id)
    return await database.fetch_one(query)


@router.put("/product/{prod_id}", response_model=Product)
async def update_prod(prod_id: int, new_prod: ProductIn):
    """Обновление товара в БД, update"""
    query = products.update().where(products.c.user_id == prod_id).values(**new_prod.dict())
    await database.execute(query)
    return {**new_prod.dict(), "prod_id": prod_id}


@router.delete("/users/{user_id}")
async def delete_prod(prod_id: int):
    """Удаление товара из БД, delete"""
    query = products.delete().where(products.c.prod_id == prod_id)
    await database.execute(query)
    return {'message': 'Product deleted'}
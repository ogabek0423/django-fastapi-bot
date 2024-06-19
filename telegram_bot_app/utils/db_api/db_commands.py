import asyncpg
from typing import Union
from asyncpg import Connection
from asyncpg.pool import Pool
from data import config

class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
        )

    async def execute(
            self,
            command,
            *args,
            fetch: bool = False,
            fetchval: bool = False,
            fetchrow: bool = False,
            execute: bool = False,
    ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())

    async def add_user(self, fullname, username, chat_id):
        sql = "INSERT INTO telegram_users (fullname, username, chat_id) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, fullname, username, chat_id, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM telegram_users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM telegram_users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM telegram_users"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, chat_id):
        sql = "UPDATE telegram_users SET username=$1 WHERE chat_id=$2"
        return await self.execute(sql, username, chat_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM telegram_users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE telegram_users", execute=True)

    async def add_product(
            self,
            name,
            category_id,
            image,
            price,
            count,
            endurance,
            description="",
    ):
        sql = "INSERT INTO products (name, category_id, image, price, count, endurance, description) VALUES($1, $2, $3, $4, $5, $6, $7) returning *"
        return await self.execute(
            sql,
            name,
            category_id,
            image,
            price,
            count,
            endurance,
            description,
            fetchrow=True,
        )

    async def get_categories(self):
        sql = "SELECT id, name FROM category"
        return await self.execute(sql, fetch=True)

    async def count_products(self, category_id):
        sql = "SELECT COUNT(*) FROM products WHERE category_id=$1"
        return await self.execute(sql, category_id, fetchval=True)

    async def get_products(self, category_id):
        sql = "SELECT * FROM products WHERE category_id=$1"
        return await self.execute(sql, category_id, fetch=True)

    async def get_product(self, product_id):
        sql = "SELECT * FROM products WHERE id=$1"
        return await self.execute(sql, product_id, fetchrow=True)

    async def drop_products(self):
        await self.execute("DROP TABLE products", execute=True)

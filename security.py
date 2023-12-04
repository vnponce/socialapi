from database import database, user_table


async def get_user(email: str):
    query = user_table.select().where(user_table.c.email == email)
    result = await database.fetch_one(query)

    if result:
        return result

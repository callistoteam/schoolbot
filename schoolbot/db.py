import aiomysql
import os

pool = None


async def connect_db():
    return await aiomysql.create_pool(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_UNAME"],
        password=os.environ["DB_PW"],
        db=os.environ["DB_DBNAME"],
        cursorclass=aiomysql.DictCursor,
        autocommit=True,
    )


async def get_user_data(id):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM `users` WHERE ID = %s;", id)
            return await cur.fetchone()


async def create_user_data(id, neis_ae, neis_se, grade, class_nm, scclass):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "INSERT INTO `users`(`id`, `neis_ae`, `neis_se`, `grade`, `class_nm`, `class`) VALUES (%s,%s,%s,%s,%s,%s);",
                (id, neis_ae, neis_se, grade, class_nm, scclass),
            )
            return


async def change_public(id, public):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "UPDATE `users` SET `public` = %s WHERE ID = %s;", (public, id)
            )
            return


async def update_school(id, neis_ae, neis_se, grade, class_nm, scclass):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "UPDATE `users` SET `neis_ae` = %s, `neis_se` = %s, `grade` = %s, `class_nm` = %s, `class` = %s WHERE ID = %s;",
                (neis_ae, neis_se, grade, class_nm, scclass, id),
            )
            return

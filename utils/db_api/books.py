from utils.db_api.main import Database


class BooksDB:
    def __init__(self, db: Database):
        self.db = db

    async def add_book(self, name):
        sql = """ INSERT INTO books (name) VALUES ($1) RETURNING id """
        return await self.db.execute(sql, name, fetchval=True)

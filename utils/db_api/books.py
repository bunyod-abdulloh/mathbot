from utils.db_api.main import Database


class BooksDB:
    def __init__(self, db: Database):
        self.db = db

    async def add_book(self, name, question_number, answer):
        sql = """ INSERT INTO books (name, question_number, answer) VALUES ($1, $2, $3) RETURNING id """
        return await self.db.execute(sql, name, question_number, answer, fetchval=True)

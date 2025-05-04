from utils.db_api.main import Database


class BooksDB:
    def __init__(self, db: Database):
        self.db = db

    async def add_book(self, name):
        sql = """ INSERT INTO books (name) VALUES ($1) RETURNING id """
        return await self.db.execute(sql, name, fetchval=True)

    async def add_question(self, book_id, book_name, question_number, answer):
        sql = """ INSERT INTO books (book_id, name, question_number, answer) VALUES ($1, $2, $3, $4) """
        await self.db.execute(sql, book_id, book_name, question_number, answer, execute=True)

    async def update_question(self, question_number, answer, book_id):
        sql = """ UPDATE books SET book_id = $3, question_number = $1, answer = $2 WHERE id = $3 """
        await self.db.execute(sql, question_number, answer, book_id, execute=True)

    async def get_book_name(self, book_id):
        sql = """ SELECT name FROM books WHERE id = $1 """
        return await self.db.execute(sql, book_id, fetchval=True)

    async def get_books(self):
        sql = """ SELECT DISTINCT ON (book_id) book_id, name, id FROM books ORDER BY book_id, id DESC """
        return await self.db.execute(sql, fetch=True)

    async def delete_book(self, book_id):
        await self.db.execute("DELETE FROM books WHERE book_id = $1", book_id, execute=True)

    async def delete_book_by_row_id(self, row_id):
        await self.db.execute("DELETE FROM books WHERE id = $1", row_id, execute=True)

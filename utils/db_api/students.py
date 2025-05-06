from utils.db_api.main_db import Database


class StudentsDB:
    def __init__(self, db: Database):
        self.db = db

    async def add_student(self, full_name, user_id):
        sql = """ INSERT INTO students (full_name, user_id) VALUES($1, $2) """
        await self.db.execute(sql, full_name, user_id, execute=True)

    async def check_student(self, user_id):
        sql = """ SELECT EXISTS (SELECT 1 FROM students WHERE user_id = $1) """
        return await self.db.execute(sql, user_id, fetchval=True)

    async def set_student_point(self, point, book_id, user_id):
        sql = """ UPDATE students SET point = $1 book_id = $2 WHERE user_id = $3 """
        await self.db.execute(sql, point, book_id, user_id, execute=True)

    async def sum_points(self, user_id):
        sql = """  """

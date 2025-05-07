from utils.db_api.main_db import Database


class StudentsDB:
    def __init__(self, db: Database):
        self.db = db

    async def add_student(self, user_id):
        sql = """ INSERT INTO students (user_id) VALUES($1) """
        await self.db.execute(sql, user_id, execute=True)

    async def add_example(self, user_id, correct, incorrect):
        sql = """ INSERT INTO students (user_id, correct, incorrect) VALUES($1, $2, $3) """
        await self.db.execute(sql, user_id, correct, incorrect, execute=True)


    async def check_student(self, user_id):
        sql = """ SELECT EXISTS (SELECT 1 FROM students WHERE user_id = $1) """
        return await self.db.execute(sql, user_id, fetchval=True)

    async def set_student_point(self, correct, incorrect, book_id, user_id):
        sql = """ UPDATE students SET correct = $1, incorrect = $2, book_id = $3 WHERE user_id = $4 """
        await self.db.execute(sql, correct, incorrect, book_id, user_id, execute=True)

    async def sum_points(self, user_id):
        sql = """ SELECT SUM(correct) FROM students WHERE user_id = $1 """
        return await self.db.execute(sql, user_id, fetchval=True)

    async def get_all_rating(self):
        sql = """
            SELECT 
                ROW_NUMBER() OVER (ORDER BY SUM(s.correct) DESC) AS row_num,
                u.telegram_id,
                u.full_name,
                SUM(s.correct) AS total_correct
            FROM students s
            JOIN users u ON s.user_id = u.id
            WHERE s.user_id IS NOT NULL
            GROUP BY s.user_id, u.full_name, u.telegram_id 
            ORDER BY total_correct DESC
        """
        return await self.db.execute(sql, fetch=True)

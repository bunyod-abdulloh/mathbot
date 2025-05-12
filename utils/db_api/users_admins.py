from utils.db_api.main_db import Database


class UsersAdminsDB:
    def __init__(self, db: Database):
        self.db = db

    # ====================== USERS ======================
    async def add_user(self, telegram_id):
        sql = "INSERT INTO users (telegram_id) VALUES ($1) ON CONFLICT (telegram_id) DO NOTHING"
        await self.db.execute(sql, telegram_id, execute=True)

    async def add_user_to_db(self, telegram_id, full_name):
        sql = """ INSERT INTO users(telegram_id, full_name) VALUES($1, $2) """
        await self.db.execute(sql, telegram_id, full_name, execute=True)

    async def set_full_name(self, full_name, user_id):
        sql = """ UPDATE users SET full_name = $1 WHERE id = $2 """
        await self.db.execute(sql, full_name, user_id, execute=True)


    async def select_user(self, telegram_id):
        sql = "SELECT id, full_name FROM users WHERE telegram_id = $1"
        return await self.db.execute(sql, telegram_id, fetchrow=True)

    async def get_full_name(self, user_id):
        sql = """ SELECT full_name FROM users WHERE id = $1 """
        return await self.db.execute(sql, user_id, fetchval=True)

    async def select_all_users(self):
        sql = "SELECT telegram_id FROM users "
        return await self.db.execute(sql, fetch=True)

    async def select_all_users_datas(self):
        sql = "SELECT telegram_id, full_name FROM users "
        return await self.db.execute(sql, fetch=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM users"
        return await self.db.execute(sql, fetchval=True)

    async def delete_user(self, telegram_id):
        sql = "DELETE FROM users WHERE telegram_id = $1"
        return await self.db.execute(sql, telegram_id, execute=True)

    async def delete_user_by_fullname(self, full_name):
        sql = """ DELETE FROM users WHERE full_name = $1 """
        result = await self.db.execute(sql, full_name, execute=True)

        # 'DELETE 1', 'DELETE 0', va hokazo bo'ladi
        deleted_count = int(result.split(" ")[1])

        return deleted_count > 0  # True bo‘lsa — o‘chirildi, False bo‘lsa — topilmadi

    async def drop_table_users(self):
        sql = "DROP TABLE users"
        return await self.db.execute(sql, execute=True)

    # ====================== ADMINS ======================
    async def add_send_status(self):
        sql = "INSERT INTO admins (status) VALUES (FALSE)"
        await self.db.execute(sql, execute=True)

    async def update_status_true(self):
        sql = "UPDATE admins SET status = TRUE"
        return await self.db.execute(sql, execute=True)

    async def update_status_false(self):
        sql = "UPDATE admins SET status = FALSE"
        return await self.db.execute(sql, execute=True)

    async def get_send_status(self):
        sql = "SELECT status FROM admins"
        return await self.db.execute(sql, fetchval=True)

    async def drop_table_admins(self):
        sql = "DROP TABLE admins"
        return await self.db.execute(sql, execute=True)

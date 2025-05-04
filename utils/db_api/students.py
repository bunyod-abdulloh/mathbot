from utils.db_api.main import Database


class StudentsDB:
    def __init__(self, db: Database):
        self.db = db

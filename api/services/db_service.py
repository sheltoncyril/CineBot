import os

from sqlmodel import Session, SQLModel, create_engine


class DBService():
    def __init__(self):
        self.db_url = f"sqlite:///{os.environ.get("DB_FILENAME", 'sqlite.db')}"
        self.engine = create_engine(self.db_url)

    def init(self, *args, **kwargs):
        SQLModel.metadata.create_all(self.engine)

    def get_session(self):
        with Session(self.engine) as session:
            yield session
            
    @property
    def session(self):
        return Session(self.engine)

    def cleanup(self):
        self.engine.close()

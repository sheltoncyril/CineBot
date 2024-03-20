import os

from sqlmodel import Session, SQLModel, create_engine


class DB():
    def __init__(self):
        self.db_url = f"sqlite:///{os.environ.get("DB_FILENAME", 'sqlite.db')}"
        self.engine = create_engine(self.db_url)

    def init(self):
        SQLModel.metadata.create_all(self.engine)

    def get_session(self):
        with Session(self.engine) as session:
            yield session
            session.commit()
            
    @property
    def session(self):
        yield self.get_session()

    def cleanup(self):
        self.engine.close()

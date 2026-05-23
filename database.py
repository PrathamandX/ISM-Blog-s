from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase,sessionmaker

SQLALCHEMY_DATABASE_URL="sqllite:///./blog.db" ##tells sqlalchemy where to connect (For postgresql just change url),
                                                ## the blog.db file will be auto created

engine=create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread":False},
)

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    with SessionLocal() as db:
        yield db

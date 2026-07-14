# create_engine - "factory class", used to connect to "mysql database"
from sqlalchemy import create_engine
#sessionmaker - used to create the sessions
#declarative_base - used to create the tables
from sqlalchemy.orm import sessionmaker,declarative_base
DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/emp_db"
# connecting to database
engine = create_engine(DATABASE_URL)
sessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base = declarative_base()
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
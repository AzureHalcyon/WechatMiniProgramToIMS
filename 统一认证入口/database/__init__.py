import sqlalchemy as sql
import sqlalchemy.ext.declarative as declarative
import sqlalchemy.orm as orm
SQLALCHEMY_DATABASE_URL = "sqlite:///./data.db"
engine = sql.create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative.declarative_base()

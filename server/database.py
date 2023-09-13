from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from configuration import configuration
from exceptions import DBSetupFailure

try:
    engine = create_engine(configuration.database_url)
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    base = declarative_base()
except Exception as e:
    raise DBSetupFailure(str(e))


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from playitloud.models import Base
import playitloud.models

DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

@pytest.fixture()
def db_session():
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
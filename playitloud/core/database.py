from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from playitloud.core.config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine)

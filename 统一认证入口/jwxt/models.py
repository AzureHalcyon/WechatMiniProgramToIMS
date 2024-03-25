import sqlalchemy.orm as orm
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
import os
import sys
from database import Base

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class UserCookies(Base):
    __tablename__ = "UserCookies"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    cookies = Column(String, nullable=False)

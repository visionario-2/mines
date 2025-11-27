from sqlalchemy import Column, Integer, String, DateTime, JSON, Numeric
from sqlalchemy.ext.declarative import declarative_base
import datetime
import json
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String, unique=True, index=True)
    balance = Column(Numeric, default=0)
    created_at = Column(DateTime, default=func.now())

class Game(Base):
    __tablename__ = "games"
    id = Column(String, primary_key=True, index=True)  # use urlsafe token as id
    user_id = Column(Integer, index=True)
    bet_amount = Column(Numeric)
    w = Column(Integer)
    h = Column(Integer)
    bombs = Column(Integer)
    bomb_positions = Column(JSON)
    opened = Column(JSON, default=list)
    state = Column(String, default="playing")  # playing, lost, cashed_out
    server_seed = Column(String)
    client_seed = Column(String)
    commit_hash = Column(String)
    created_at = Column(DateTime, default=func.now())

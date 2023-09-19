from sqlalchemy import Column, Integer, String, Date, DateTime, LargeBinary
import datetime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    surname = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    password = Column(String(200), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    date_of_birth = Column(String(100))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    avatar = Column(String(600), nullable=True)
    snaps = Column(Integer, nullable=True)
    followers = Column(Integer, nullable=True)
    following = Column(Integer, nullable=True)
    bio = Column(String(200), nullable=True)  

    def __init__(self, username, surname, name, password, email, date_of_birth,
                 snaps=None, followers=None, following=None, bio=None,
                 created_at=None, avatar=None):
        self.username = username
        self.surname = surname
        self.name = name
        self.password = password
        self.email = email
        self.date_of_birth = date_of_birth
        self.created_at = created_at
        self.avatar = avatar
        self.snaps = snaps
        self.followers = followers
        self.following = following
        self.bio = bio

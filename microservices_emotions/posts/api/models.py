import os
from datetime import datetime

from quart import Quart, render_template
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy import update
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize SQLAlchemy with a test database
base = os.path.abspath(os.path.dirname(__name__))
database_folder = os.path.join(base, "posts/database/")
os.makedirs(database_folder, exist_ok=True)
database_path = os.path.join(database_folder, "test.db")
DATABASE_URL = f"sqlite+aiosqlite:///{database_path}"
engine = create_async_engine(DATABASE_URL, future=True, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, index=True)
    email = Column(String(64), unique=True, index=True)
    password_hash = Column(String(128))
    profile_image = Column(String(20), nullable=False, default="default.png")

    def __init__(self, username, email, password, profile_image=None):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.profile_image = profile_image

    def __repr__(self):
        return f"Username {self.username} {self.profile_image}"

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def json(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password_hash,
            "profile_image": self.profile_image
        }


class BlogPost(Base):

    __tablename__ = "post"

    users = relationship(User)
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    date = Column(DateTime, nullable=False, default=datetime.now())
    title = Column(String(140), nullable=False)
    text = Column(Text, nullable=False)
    emotion = Column(String, nullable=False, default="joy")

    def __init__(self, user_id, title, text, emotion="joy"):
        self.user_id = user_id
        self.title = title
        self.text = text
        self.emotion = emotion

    def __repr__(self):
        return f"Post ID: {self.id}"

    def json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "text": self.text,
            "date": self.date,
            "emotion": self.emotion
        }

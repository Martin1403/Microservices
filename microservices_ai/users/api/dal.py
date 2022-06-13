from contextlib import asynccontextmanager

from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

from users.api.models import async_session, User


class SomeException(Exception):
    pass


class UserDAL(object):
    """User Data Access Layer"""
    def __init__(self, session):
        self.db_session = session

    async def create_user(self, input):
        user = User(**input)
        try:
            self.db_session.add(user)
            await self.db_session.commit()
            return user
        except IntegrityError:
            return

    async def get_user_email(self, email):
        result = await self.db_session.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def get_user_by_id(self, id):
        result = await self.db_session.execute(select(User).where(User.id == id))
        return result.scalars().first()

    async def update_user(self, kwargs):
        try:
            user = await self.get_user_id(kwargs.get('id'))
            user.username = kwargs.get('new_username') or user.username
            user.password_hash = generate_password_hash(kwargs.get("password")) or user.password_hash
            user.email = kwargs.get("email") or user.email
            user.picture = kwargs.get("picture") or user.picture
            await self.db_session.flush()
            return user
        except SomeException:
            return

    async def delete_user_id(self, id):
        user = await self.get_user_id(id=id)
        await self.db_session.delete(user)


@asynccontextmanager
async def user_dal():
    async with async_session() as session:
        async with session.begin():
            yield UserDAL(session)

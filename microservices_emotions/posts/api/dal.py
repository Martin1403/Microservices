from contextlib import asynccontextmanager

from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound

from .models import User, async_session, BlogPost


class UserDAL(object):
    """Data Access Layer for User"""
    def __init__(self, db_session):
        self.db_session = db_session

    async def create_user(self, username, email, password, profile_image=None):
        query_result = await self.db_session.execute(select(User).order_by(User.id))
        users_list = [user.json() for user in query_result.scalars().all()]
        usernames = [user["username"] for user in users_list]
        emails = [user["email"] for user in users_list]
        if username not in usernames and email not in emails:
            new_user = User(
                username=username,
                email=email,
                password=password,
                profile_image=profile_image
            )
            self.db_session.add(new_user)
            await self.db_session.flush()
            return new_user.json()
        raise ValueError("Username or password already in database.")

    async def get_all_users(self):
        query_result = await self.db_session.execute(select(User).order_by(User.id))
        return {"users": [user.json() for user in query_result.scalars().all()]}

    async def get_user_by_email(self, email, password):
        query = select(User).where(User.email == email)
        try:
            query_result = await self.db_session.execute(query)
            user = query_result.one()
            if user[0].check_password(password=password):
                return user[0].json()
            else:
                raise ValueError("Password is incorrect.")
        except NoResultFound:
            raise ValueError("Email not found.")

    async def get_user_by_username(self, username):
        query = select(User).where(User.username == username)
        try:
            query_result = await self.db_session.execute(query)
            user = query_result.one()
            return user[0].json()
        except NoResultFound:
            raise ValueError(f"No user {username} found.")

    async def update_user_by_username(self, data):
        query = select(User).where(User.username == data.username)
        try:
            query_result = await self.db_session.execute(query)
            user = query_result.one()[0]

            user.profile_image = data.new_picture
            user.email = data.new_email
            user.username = data.new_username

            await self.db_session.flush()
            return user.json()
        except NoResultFound:
            raise ValueError(f"No user {data.username} found.")


class BlogPostDAL(object):
    """Data Access Layer for BlogPosts."""
    def __init__(self, db_session):
        self.db_session = db_session

    async def create_blog_post_username(self, username, title, text, emotion):
        query = select(User).where(User.username == username)
        try:
            query_result = await self.db_session.execute(query)
            user = query_result.one()
            user = user[0].json()
            post = BlogPost(user_id=user["id"], title=title, text=text, emotion=emotion)
            self.db_session.add(post)
            await self.db_session.flush()
            return post.json()
        except (NoResultFound, KeyError):
            raise ValueError(f"No user {username} found.")

    async def get_all_posts_by_username(self, username):
        query = select(User).where(User.username == username)
        try:
            query_result = await self.db_session.execute(query)
            user = query_result.one()
            user = user[0].json()
            query = select(BlogPost).where(
                BlogPost.user_id == user["id"]).order_by(BlogPost.date.desc())

            query_result = await self.db_session.execute(query)
            return {"posts": [post.json() for post in query_result.scalars().all()]}

        except (NoResultFound, KeyError):
            raise ValueError(f"No user {username} found.")

    async def update_blog_post_id(self, id, title, text):
        try:
            query = select(BlogPost).where(BlogPost.id == id)
            query_result = await self.db_session.execute(query)
            blog_post = query_result.one()
            blog_post = blog_post[0]
            blog_post.title = title
            blog_post.text = text
            await self.db_session.flush()
            return blog_post.json()
        except (NoResultFound, ValueError, KeyError):
            raise ValueError(f"No blog post id: {id} found.")

    async def delete_blog_post_id(self, id):
        try:
            query = select(BlogPost).where(BlogPost.id == id)
            query_result = await self.db_session.execute(query)
            blog_post = query_result.one()
            blog_post = blog_post[0]
            await self.db_session.delete(blog_post)
        except (NoResultFound, ValueError, KeyError):
            raise ValueError(f"No blog post id: {id} found.")


@asynccontextmanager
async def user_dal():
    async with async_session() as session:
        async with session.begin():
            yield UserDAL(session)


@asynccontextmanager
async def blog_post_dal():
    async with async_session() as session:
        async with session.begin():
            yield BlogPostDAL(session)

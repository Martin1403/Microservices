from ariadne import MutationType

from users.api.dal import user_dal

mutation = MutationType()


@mutation.field("CreateUser")
async def create_user_resolver(*_, input):
    async with user_dal() as ud:
        user = await ud.create_user(input)
    return user if user else None

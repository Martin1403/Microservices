from ariadne import QueryType

from users.api.dal import user_dal

query = QueryType()


@query.field('user')
async def resolve_user_by_id(*_, id):
    """
query GetUserById($id: ID!){
  user(id: $id) {
    id
    username
    email
    password_hash
    date
  }
}
{
  "id": "NP3cF9KfcY5mrzpjRSNDJf"
}
{
	"operationName": "GetUserById",
	"query": "query GetUserById($id: ID!) {\n  user(id: $id) {\n    id\n    username\n    email\n    password_hash\n    date\n  }\n}\n",
	"variables": {
		"id": "NP3cF9KfcY5mrzpjRSNDJf"
	}
}
    """
    async with user_dal() as ud:
        user = await ud.get_user_by_id(id)
    return user

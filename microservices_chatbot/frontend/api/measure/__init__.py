GET_POSTS_BY_USER_ID_COMMAND = """
query {
  posts(user_id: "ID") {
    id
    user_text
    user_date
    ai_text
    ai_date
  }
}
"""
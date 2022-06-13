CREATE_POST_COMMAND = """
mutation CreatePost($input: CreatePostInput) {
  post: CreatePost(input: $input) {
    user_id
  }
}
"""
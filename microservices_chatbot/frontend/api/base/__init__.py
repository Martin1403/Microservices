CREATE_USER_COMMAND = """
mutation CreateUser($input: CreateUserInput) {
  user: CreateUser(input: $input) {
    id
    username
    email
    password_hash
    date
  }
}
"""
LOGIN_USER_COMMAND = """
{
  login(email:"EMAIL", 
    password:"PASSWORD"){
    id
    username
    picture
  } 
}
"""
UPDATE_USER_COMMAND = """
mutation UpdateUser($input: UpdateUserInput) {
  update: UpdateUser(input: $input) {
    id
    username
    email
    password_hash
    date
    picture
  }
}
"""
DELETE_USER_COMMAND = """
{
  delete(id: "ID"){
    id
    username
  }
}
"""

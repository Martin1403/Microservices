import os

# Url for all endpoints:
url_for_jobs = "http://jobs-service-c:5001/graphql" \
    if os.environ.get("DOCKER") else "http://127.0.0.1:5001/graphql"

url_for_users = "http://users-service-c:5002" \
    if os.environ.get("DOCKER") else "http://127.0.0.1:5002"

# Headers:
headers = {'accept': 'application/json'}
content_headers = {'accept': 'application/json', 'Content-Type': 'application/json'}

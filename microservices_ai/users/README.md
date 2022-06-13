Database Manager
================
![](static/images/logo.png)
![](static/images/graphql-icon.png)
### Venv:
###### python3.9
###### /users
```
python -m venv .venv && \
source .venv/bin/activate && \
pip install -U pip && \
pip install -r requirements.txt
```
### Run:
###### /
```
export QUART_APP=users.app:app && \
export QUART_ENV=development && \
quart run -h "127.0.0.1" -p 5002
```
### Tests:
###### /
- ###### Test async:
    ````
    export QUART_APP=users.app:app && \
    export QUART_ENV=development && \
    quart test-async
- ###### Initialize database:
    ````
    export QUART_APP=users.app:app && \
    export QUART_ENV=development && \
    quart init-db  
    ````
- ###### Test database access layer:
    ````
    export QUART_APP=users.app:app && \
    export QUART_ENV=development && \
    quart test-dal
### Docker:
###### /app
```
docker build -t app . && \
docker run -it --rm -p 5001:5001 app && \
docker rmi app --force
```
**Note:** 
###### Help:
- ###### / inside root directory or cd /xxx  
###### [Links:]()
- ###### [Link]()
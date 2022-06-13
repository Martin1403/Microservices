Router ![](static/images/logo.png)
======
### Venv:
###### python3.9
###### /router
```
python -m venv .venv && \
source .venv/bin/activate && \
pip install -U pip && \
pip install -r requirements.txt
```
### Run:
###### /
```
export QUART_APP=router.app:app && \
export QUART_ENV=development && \
quart run -h "127.0.0.1" -p 5001
```
### Tests:
###### /
- ###### Test async:
    ````
    export QUART_APP=app.app:app && \
    export QUART_ENV=development && \
    quart test-async
    ````
### Docker:
###### /router
```
docker build -t router . && \
docker run -it --rm -p 5001:5001 router && \
docker rmi router --force
```
**Note:** 
###### Help:
- ###### / inside root directory or cd /xxx  
###### [Links:]()
- ###### [Link]()
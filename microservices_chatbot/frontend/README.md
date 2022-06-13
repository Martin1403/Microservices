Frontend Quart app
==================
![](static/images/screen.png)

### Venv:
###### python3.7-9
###### /frontend
```
python -m venv .venv && \                                                     
source .venv/bin/activate && \
pip install -U pip && \
pip install -r requirements.txt
```
### Run:
###### /
```
export QUART_APP=frontend.app:app && \
export QUART_ENV=development && \
quart run -h "127.0.0.1" -p 5000
```
### Docker:
###### /frontend
```
docker build -t frontend . && \
docker run -it --rm -p 5000:5000 frontend && \
docker rmi app --force
```
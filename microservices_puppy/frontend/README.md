Frontend Webapp
===============
![](static/img.png)

### Venv:
###### python3.9
###### /frontend
```shell
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
### Run:
###### /
```shell
export FLASK_ENV=development && \
export FLASK_APP=frontend && \
flask run --reload -h localhost -p 5000
```
### Docker:
###### /frontend
```shell
docker build -t frontend . && \
docker run -it -p 5000:5000 --rm frontend && \
docker rmi frontend --force
```




### Run:
```shell
cd frontend
python -m venv .venv
source .venv/bin/activate 
cd ..
python frontend
```
### Docker:
```shell
cd frontend && \
docker build -t frontend . && \
docker run -it -p 5000:5000 --rm frontend && \
docker rmi frontend --force 
```
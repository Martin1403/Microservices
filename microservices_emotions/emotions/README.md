

### Run:
```shell
cd emotions
python -m venv .venv
source .venv/bin/activate 
cd ..
python emotions
```
### Docker:
```shell
cd emotions && \
docker build -t emotions . && \
docker run -it -p 5002:5002 --rm emotions && \
docker rmi emotions --force 
```
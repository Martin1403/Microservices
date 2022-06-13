

### Run:
```shell
cd posts
python -m venv .venv
source .venv/bin/activate 
cd ..
python posts
```
### Docker:
```shell
cd posts && \
docker build -t posts . && \
docker run -it -p 5001:5001 --rm posts && \
docker rmi posts --force 
```
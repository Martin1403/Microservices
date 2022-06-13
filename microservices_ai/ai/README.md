Tensorflow memory network ![](static/images/logo.png)
=========================
### Venv:
###### python3.7
###### /chat
```
python -m venv .venv && \
source .venv/bin/activate && \
pip install -U pip && \
pip install -r requirements.txt
```
### Run:
###### /
```
export QUART_APP=chat.app:app && \
export QUART_ENV=development && \
quart run -h "127.0.0.1" -p 5003
```
### Tests:
###### /
- ###### Test async:
    ````
    export QUART_APP=chat.app:app && \
    export QUART_ENV=development && \
    quart test-async
    ````
### Docker:
###### /chat
```
docker build -t chat . && \
docker run -it --rm -p 5003:5003 chat && \
docker rmi chat --force
```
**Note:**
Tensorflow1.1x Seq2Seq Attention with memory network (Gated/GRU)
###### Help:
- ###### / inside root directory or cd /xxx  
###### [Links:]()
- ###### [Link](https://github.com/Martin1403/Tensorflow1.15.x-MemoryNetwork) Train with your own data...

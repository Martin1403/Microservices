DeepSpeech STT API ![](static/images/logo.png)
==================
### Venv:
###### python3.9
###### /dstt
```
python -m venv .venv && \
source .venv/bin/activate && \
pip install -U pip && \
pip install -r requirements.txt
```
### Scorer:
###### /stt
```
wget -O model/output_graph.scorer https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer
```
### Run:
###### /
```
export QUART_APP=stt.app:app && \
export QUART_ENV=development && \
quart run -h "127.0.0.1" -p 5001
```
### Tests:
###### /
- ###### Test async:
    ````
    export QUART_APP=stt.app:app && \
    export QUART_ENV=development && \
    quart test-async
    ````
- ###### Test model:
    ````
    export QUART_APP=stt.app:app && \
    export QUART_ENV=development && \
    quart test-model
    ````  
### Docker:
###### /stt
```
docker build -t stt . && \
docker run -it --rm -p 5001:5001 stt && \
docker rmi stt --force
```
**Note:** 
Mozilla DeepSpeech-0.9.3
Custom Tensorflow-lite model used, you can train your own...
###### Help:
- ###### / inside root directory or cd /xxx  
###### [Links:]()
- ###### [Link](https://github.com/mozilla/DeepSpeech/releases/tag/v0.9.3) GithubLink to DeepSpeech 0-9-3...
- ###### [Link](https://github.com/Martin1403/STT-Tensorflow1.15.x-DeepSpeech) Train DeepSpeech model with your own data...
- ###### [Link](https://github.com/Martin1403/Tensorflow1.15.x-MemoryNetwork) Train Seq2seq model with your own data...
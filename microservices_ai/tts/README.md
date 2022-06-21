TTS ![](static/images/logo.png)
===
![](static/images/screen.png)
###### venv: python3.9
###### /
```
python -m venv tts/.venv && \
source tts/.venv/bin/activate && \
pip install -U pip && \
pip install -r tts/requirements.txt && \
pip install torch==1.8.1+cpu torchvision==0.9.1+cpu torchaudio==0.8.1 -f https://download.pytorch.org/whl/lts/1.8/torch_lts.html
```
### Unpack voices:
###### / 
###### apt-get install p7zip-full
```
7za x tts/voices/voices.7z.001 -otts/voices/
```
### Run:
###### /
```
source tts/.venv/bin/activate && \
export QUART_APP=tts.app:app && \
export QUART_ENV=development && \
quart run -h "127.0.0.1" -p 5003
```
### Tests:
###### /
- ###### Test async:
    ````
    export QUART_APP=tts.app:app && \
    export QUART_ENV=development && \
    quart test-async
    ````
### Docker:
###### /tts
```
docker build -t tts . && \
docker run -it --rm -p 5003:5003 tts && \
docker rmi tts --force
```
**Note:** 
###### Help:
- ###### / inside root directory or cd /xxx  
###### [Links:]() 
- ###### [Link](https://drive.google.com/drive/folders/10_ZNA4PxF3QtYrBBEwjAFQfnhH9E1yqY?usp=sharing) Download more voices
- ###### [Link](https://github.com/rhasspy/larynx) GitHub link to Larynx

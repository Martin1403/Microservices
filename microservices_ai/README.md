Microservices Ai
================
![](frontend/static/images/flowchart.png)
### Run:
```
git clone https://github.com/Martin1403/Microservices.git 
cd Microservices/microservices_ai && \
docker-compose up --build

docker rmi $(docker images --format="{{.ID}}" | head -n 4) --force && \
docker rm $(docker ps -aq) --force && \
docker network prune && \
docker volume prune
```
**Note:**
- ###### [Link](https://github.com/Martin1403/Tensorflow-1.1X/tree/master/chatbot_with_memory) train your own ai-model ...
- ###### [Link](https://github.com/Martin1403/Tensorflow-1.1X/tree/master/deepspeech_train) train your own stt-model ...

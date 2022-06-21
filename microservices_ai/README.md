Ai
==
![](flowchart.png)
### Run:
```
git clone https://github.com/Martin1403/Microservices.git 
cd Microservices/microservices_ai && \
docker-compose up --build


docker-compose down && \
docker rmi $(docker images --format="{{.ID}}" microservices-ai_*) --force && \
docker volume prune
```


### Docker:
```shell
docker network create --driver bridge micro_network
cd user
docker build -t userapi .
cd book
docker build -t bookapi .
cd order
docker build -t orderapi .
cd frontend
docker build -t frontendapi .

docker run -p 5001:5001 -d --name user-service-c --network=micro_network userapi
docker run -p 5002:5002 -d --name book-service-c --network=micro_network bookapi
docker run -p 5003:5003 -d --name order-service-c --network=micro_network orderapi
docker run -p 5000:5000 -d --name frontend-service-c --network=micro_network frontendapi

```

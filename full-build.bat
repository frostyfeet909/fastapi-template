docker rm backend && docker rm init_backend && docker rm postgres && docker rm redis && docker rm worker
docker image rm backend && docker image rm init_backend && docker image rm postgres && docker image rm redis && docker image rm worker
docker volume rm postgres && docker volume rm mongo
docker image prune -a
docker-compose -f docker-compose.yml build
docker-compose up

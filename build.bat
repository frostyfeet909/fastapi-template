docker rm backend && docker rm init_backend && docker rm worker
docker-compose -f docker-compose.yml build
docker-compose -p "myapp" up
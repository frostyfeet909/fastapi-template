docker-compose -f docker-compose.yml -f docker-compose.override.yml down
docker-compose -f docker-compose.yml -f docker-compose.override.yml build
docker image prune -f
docker-compose -f docker-compose.yml -f docker-compose.override.yml up

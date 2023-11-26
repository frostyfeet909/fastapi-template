set containter=pgadmin
docker compose -f docker-compose.yml -f docker-compose.override.yml build %containter%
docker image prune -f
docker compose -f docker-compose.yml -f docker-compose.override.yml up --no-deps -d %containter%
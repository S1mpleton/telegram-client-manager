#run docker-container
docker build -t redis .
docker run -d --name redis-container -p 6300:6300 my-redis


docker build .

docker build --tag birdid:0.0.1 .
docker run --name birdid-api -p 5000:5000 birdid:0.0.1

docker build -t skiddaw/cheers2019 .

docker build -t skiddaw/birdy:latest .
docker run -d -p 5000:5000 skiddaw/birdy
docker run -d -p 5000:5000 skiddaw/birdy:latest

docker build -t shykes/myapp:1.0.2 -t shykes/myapp:latest .

docker run -it --rm skiddaw/cheers2019

docker build -t flask-sample-one:latest .
docker run -d -p 5000:5000 flask-sample-one

docker ps -a

docker logs f63b6b38f17d
# Twelve Factor App Django Deployment ( tfa-django )

This repository is meant to surver the purpose of illustrating how to run a local development environment with [Docker] (https://docs.docker.com/get-started/) that'll integrate well into a [Kubernetes](https://kubernetes.io/docs/tutorials/kubernetes-basics/) cluster.

## Pulling and running the container in your terminal

`tfa-django` requires PostgreSQL and Redis to run. `tfa-django` has a single page that counts the number of times it
has accessed the Database and Redis. Illistrating that the network docker is using to run the containers is available 
and responsive to our actions

```
# Setup Data Stores
$ docker run --name tfa-postgresql -p 5432:5432 -e POSTGRES_USER=db-user -e POSTGRES_PASSWORD=db-pass -e POSTGRES_DB=tfa -d postgres
$ docker run --rm --name tfa-redis -p 6379:6379 -d redis

# Setup ENVVars for the Containers
$ export CACHE_IP=$(docker inspect tfa-redis|jq -r '.[0].NetworkSettings.Networks.bridge.IPAddress')
$ export DB_IP=$(docker inspect tfa-postgresql|jq -r '.[0].NetworkSettings.Networks.bridge.IPAddress')

# Once to migrate the database
$ docker run --rm --name tfa-django -e PSQL_URL="postrgesql://db-user:db-pass@$DB_IP:5432/tfa" -e REDIS_URL="redis://$CACHE_IP:6379/0" jbcurtin/tfa-django python3 ./manage.py migrate

# Once to start the server
$ docker run --name tfa-django -p 8000:8000 -e DEBUG='t' -e PSQL_URL="postrgesql://db-user:db-pass@$DB_IP:5432/tfa" -e REDIS_URL="redis://$CACHE_IP:6379/0" -d jbcurtin/tfa-django ./.local/bin/gunicorn lab.wsgi -b 0.0.0.0
```

Navigate to `http://localhost:8000/webservice/counter.txt` from Firefox, IE Edge, Chrome, Opera or another browser of choice

## Using Docker Compose

```
$ docker-compose run webservice python3 ./manage.py migrate
$ docker-compose up
```

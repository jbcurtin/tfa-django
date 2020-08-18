FROM debian:bullseye

RUN export DEBIAN_FRONTEND='noninteractive'
RUN export LC_CTYPE='en_US.UTF-8'
RUN export LC_ALL='en_US.UTF-8'

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install apt-transport-https ca-certificates build-essential curl -y

RUN echo "deb [arch=amd64] http://apt.postgresql.org/pub/repos/apt bullseye-pgdg main" > /etc/apt/sources.list.d/pgdg.list
RUN curl -sSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN apt-get update
RUN apt-get install postgresql-server-dev-12 -y
RUN apt-get install python3-pip -y
RUN mkdir -p /opt/webservice
RUN adduser --home /home/web --disabled-password --gecos "" --shell /bin/bash web 

ENV PSQL_URL=
ENV REDIS_URL=

USER web
WORKDIR /home/web
RUN pip install django requests django_redis redis psycopg2 gunicorn
COPY --chown=web:web ./lab ./

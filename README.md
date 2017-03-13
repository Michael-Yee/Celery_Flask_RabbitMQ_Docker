# Basic Celery, Flask and RabbitMQ Docker Set-Up

** WORK IN PROGRESS DOC ***

Install Docker

Ubuntu - https://docs.docker.com/engine/installation/linux/ubuntu/
Windows - https://docs.docker.com/docker-for-windows/

Install Docker Compose

https://docs.docker.com/compose/install/

curl -L https://github.com/docker/compose/releases/download/1.11.2/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

```
Build and run your app with docker-compose
docker-compose build

Build and run your app with docker-compose
docker-compose up -d (-d flag for “detached” mode)

Send requests to the app
http://localhost:5000/ or http://0.0.0.0:5000/ 

RabbitMQ manager
http://localhost:15672/ or http://0.0.0.0:15672/ 

If you are running the project locally and have flower installed, run flower -A celery_init --port=5555 and open http://localhost:5555/ to monitor RabbitMQ

Useful commands

To list all docker-compose cache
docker-compose ps

To stop the processes using following command
docker-compose stop

To remove docker-compose cache
docker-compose rm
```

Errors

Error 
Can not write to /usr/local/bin

Fix

sudo chown -R $(whoami) /usr/local/bin

---

ERROR: for rabbitmq  Cannot start service rabbitmq: driver failed programming external connectivity on endpoint celeryflaskrabbitmq_rabbitmq_1 (ca76c5a8da251366e3414ee63d3b757ff227bb496545c9a8640341b5a95d521a): Error starting userland proxy: listen tcp 0.0.0.0:5672: bind: address already in use
ERROR: Encountered errors while bringing up the project.

Fix

sudo lsof -i :5672 | grep LISTEN

michael@michael-Gazelle:~$ sudo lsof -i :5672 | grep LISTEN
[sudo] password for michael: 
beam.smp 1279 rabbitmq   55u  IPv6  18885      0t0  TCP *:amqp (LISTEN)

sudo kill 1279

---

Error: docker-compose

ERROR: Service 'microservice' failed to build: containerd: container not started

Fix
https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-16-04

curl -L "https://github.com/docker/compose/releases/download/1.8.1/docker-compose-$(uname -s)-$(uname -m)" > ./docker-compose
sudo mv ./docker-compose /usr/bin/docker-compose
sudo chmod +x /usr/bin/docker-compose
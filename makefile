appname = burgerorderer
confile = $(appname).yaml

run:
	docker compose -f $(confile) up

build: 
	docker compose -f $(confile) build

overview:
	docker images
	docker ps -a

clean:
	docker compose -f $(confile) down

deepclean: clean
	docker rmi -f $(appname)
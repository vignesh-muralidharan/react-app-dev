all: prepare
# test clean package install

prepare:
	@docker pull cryonicstrider/python-docker:v3
	@docker volume create mysql
	@docker volume create mysql_config
	@docker network ls | grep mysqlnet > /dev/null || docker network create mysqlnet 
	@docker stop mysqldb || true
	@docker stop rest-server-wcon || true
	@docker tag cryonicstrider/python-docker:v3 cryonicstrider/python-docker:latest
	@docker run --rm -d -v mysql:/var/lib/mysql -v mysql_config:/etc/mysql -p 3300:3300 --network mysqlnet --name mysqldb -e MYSQL_ROOT_PASSWORD=p@ssw0rd1 mysql
	@docker run --rm -d --network mysqlnet --name rest-server-wcon --publish 8000:5000 cryonicstrider/python-docker

clean:
	@docker stop mysqldb || true
	@docker stop rest-server-wcon || true


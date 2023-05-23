all: prepare
# test clean package install

prepare: prepareDB prepareRest
	@docker pull cryonicstrider/flask-react:v1
	@docker tag cryonicstrider/flask-react:v1 cryonicstrider/flask-react:latest
	@docker stop frontend-app || true
	@docker run --rm -d --network mysqlnet --name frontend-app -p 3000:3000 cryonicstrider/flask-react:latest

prepareDB:
	@docker volume create mysql || True
	@docker volume create mysql_config || true
	@docker network ls | grep mysqlnet > /dev/null || docker network create mysqlnet 
	@docker stop mysqldb || true
	@docker run --rm -d -v mysql:/var/lib/mysql -v mysql_config:/etc/mysql -p 3300:3300 --network mysqlnet --name mysqldb -e MYSQL_ROOT_PASSWORD=p@ssw0rd1 mysql

prepareRest:
	@docker pull cryonicstrider/python-docker:v3
	@docker tag cryonicstrider/python-docker:v3 cryonicstrider/python-docker:latest
	@docker stop rest-server-wcon || true
	@docker run --rm -d --network mysqlnet --name rest-server-wcon --publish 8000:5000 cryonicstrider/python-docker

clean:
	@docker stop mysqldb || true
	@docker stop rest-server-wcon || true
	@docker stop frontend-app || true

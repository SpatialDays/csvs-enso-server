build:
	docker-compose build

up:
	docker-compose up -d app

test: up
	docker-compose run --rm --no-deps --entrypoint=pytest app /tests/unit /tests/integration /tests/e2e -v

unit-tests:
	docker-compose run --rm --no-deps --entrypoint=pytest app /tests/unit -v

integration-tests: up
	docker-compose run --rm --no-deps --entrypoint=pytest app /tests/integration -v

e2e-tests: up
	docker-compose run --rm --no-deps --entrypoint=pytest app /tests/e2e -v

logs:
	docker-compose logs app | tail -100

down:
	docker-compose down --remove-orphans

all: down build up test
build:
	docker-compose build app

local-bash:
	docker-compose exec app /bin/bash
logs:
	docker-compose logs --follow app

e2e:
	docker-compose exec app coverage run -m pytest tests/e2e -v -x
	docker-compose exec app coverage xml --ignore-errors
	@echo "Total Python coverage:" `docker-compose exec app coverage report --precision=2 | tail -n 1 | awk '{ print $4 }'`

integration:
	docker-compose exec app pytest tests/integration -v -x

unit:
	docker-compose exec app coverage run -m pytest tests/unit -v -x
	docker-compose exec app coverage xml --ignore-errors
	@echo "Total Python coverage:" `docker-compose exec app coverage report --precision=2 | tail -n 1 | awk '{ print $4 }'`

test:
	docker-compose exec app coverage run -m pytest tests/ -v -x --ignore=tests/integration
	docker-compose exec app coverage xml --ignore-errors
	@echo "Total Python coverage:" `docker-compose exec app coverage report --precision=2 | tail -n 1 | awk '{ print $4 }'`

pre-commit-install:
	docker-compose exec app pre-commit install

start-local:
	docker-compose up -d

stop:
	docker-compose down

build:
	docker-compose build block_tracker

local-bash:
	docker-compose exec block_tracker /bin/bash
logs:
	docker-compose logs --follow block_tracker

e2e:
	docker-compose exec block_tracker coverage run -m pytest tests/e2e -v -x
	docker-compose exec block_tracker coverage xml --ignore-errors
	@echo "Total Python coverage:" `docker-compose exec block_tracker coverage report --precision=2 | tail -n 1 | awk '{ print $4 }'`

integration:
	docker-compose exec block_tracker pytest tests/integration -v -x

unit:
	docker-compose exec block_tracker coverage run -m pytest tests/unit -v -x
	docker-compose exec block_tracker coverage xml --ignore-errors
	@echo "Total Python coverage:" `docker-compose exec block_tracker coverage report --precision=2 | tail -n 1 | awk '{ print $4 }'`

test:
	docker-compose exec block_tracker coverage run -m pytest tests/ -v -x --ignore=tests/integration
	docker-compose exec block_tracker coverage xml --ignore-errors
	@echo "Total Python coverage:" `docker-compose exec block_tracker coverage report --precision=2 | tail -n 1 | awk '{ print $4 }'`

pre-commit-install:
	docker-compose exec block_tracker pre-commit install

start-local:
	docker-compose up -d

stop:
	docker-compose down

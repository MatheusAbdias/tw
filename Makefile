pre_commit:
	@pre-commit run -a

test: dc_up
	@pytest -n 4 --cov=src --cov-report=term-missing --cov-report=html

dc_up:
	@docker compose up -d

dc_down:
	@docker compose down -v

messages:
	@poetry run manage makemessages -l pt_BR

migration:
	@poetry run manage makemigrations

migrate:
	@poetry run manage migrate

server: dc_up migrate
	@poetry run manage runserver

.PHONY: test pre_commit dc_up dc_down messages migration server migrate

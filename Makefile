format:
	black . --exclude=migrations $(ARGS)

build:
	docker-compose -f docker-compose.yml up --force-recreate --build $(ARGS)

up:
	docker-compose -f docker-compose.yml up $(ARGS)

down:
	docker-compose -f docker-compose.yml down $(ARGS)

db:
	docker-compose -f docker-compose.yml up -d db $(ARGS)

makemigrations:
	docker-compose run app alembic revision --autogenerate -m "${name}"

migrate:
	docker-compose run app alembic upgrade head

downgrade:
	docker-compose run app alembic downgrade -${times}

alembic-history:
	docker-compose run app alembic history
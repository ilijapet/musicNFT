.PHONY: server
server:
	poetry run python -m backend.manage runserver

.PHONY: shell
shell:
	poetry run python -m backend.manage shell

.PHONY: install
install:
	poetry install

.PHONY: migrations
migrations:
	poetry run python -m backend.manage makemigrations
	poetry run python -m backend.manage migrate

.PHONY: update
update: install migrations ;

.PHONY: env
env:
	poetry shell

.PHONY: deact
deact:
	poetry exit



# Poetry commands
.PHONY: env
env:
	poetry shell

.PHONY: deact
deact:
	poetry exit


# Django commands
# Run Django server
.PHONY: server
server:
	poetry run python -m backend.manage runserver

# Run Django shell
.PHONY: shell
shell:
	poetry run python -m backend.manage shell

# Install dependencies
.PHONY: install
install:
	poetry install

# Run Django migrations
.PHONY: migrations
migrations:
	poetry run python -m backend.manage makemigrations; poetry run python -m backend.manage migrate

# Install dependencies and run migrations
.PHONY: update
update: install migrations install-pre-commit;

.PHONY: install-pre-commit
install-pre-commmit:
	poetry run pre-commit uninstall; poetry run pre-commit install

.PHONY: lint
lint:
	poetry run pre-commit run --all-files





pre_install:
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
	sudo npm i -g serverless

install:
	npm install
	poetry install

test:
	poetry run pytest

ci:
	poetry run pytest --cov=noverde_challenge --black --mypy --pydocstyle --pycodestyle --ignore=node_modules

serverless_pre_install:
	poetry export --without-hashes -f requirements.txt -o requirements.txt

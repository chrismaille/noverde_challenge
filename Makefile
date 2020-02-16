pre_install:
	pip install -U --user pip
	pip install -U --user poetry
	sudo npm i -g serverless
	touch requirements.txt

install:
	poetry install
	npm install

test:
	poetry run pytest

ci:
	poetry run pytest --cov=noverde_challenge --black --mypy --pydocstyle --pycodestyle --ignore=node_modules
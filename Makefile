.PHONY: help
help: ## Display this help screen.
	@grep -E '^\S.+:.*?## .*$$' Makefile | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: pyenv-virtualenv
pyenv-virtualenv:  ## Create a virtual environment managed by pyenv-virtualenv.
	pyenv install --skip-existing 3.9.12
	pyenv virtualenv 3.9.12 email-forwarding-lambda
	echo "email-forwarding-lambda" > .python-version

.PHONY: pyenv-virtualenv-delete
pyenv-virtualenv-delete:  ## Delete a virtual environment managed by pyenv-virtualenv.
	pyenv virtualenv-delete `cat .python-version`
	rm .python-version

.PHONY: dev
dev:  ## Install all packages.
	pip install --requirement requirements.txt
	pip-sync requirements.txt

.env:  ## Create .env file suitable for development.
	printf "LOG_LEVEL=DEBUG\n" > .env

requirements.txt: requirements.in;
	pip-compile requirements.in --generate-hashes

email_forwarding.zip: email_forwarding.py;
	zip email_forwarding.zip email_forwarding.py

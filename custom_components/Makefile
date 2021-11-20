.PHONY: help init style format test test-functional test-unit run security

# detect Github Actions
GITHUB_ACTIONS ?= false

# HELP
# This will output the help for each task
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html

# target names are selected based on https://gazr.io
help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-z%A-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

init: ## install/upgrade pip dependencies
	pip3 install --upgrade --requirement ./requirements-dev.txt

style: ## run syntax/style check etc. (requires flake8 and black installed)
	black --version
	black --diff --check ./
	flake8 --version
	flake8 --show-source --statistics ./

format: ## apply autoformatter (requires yapf installed)
	black --version
	black ./

test: test-unit style ## run all local tests (all except functional)

# set environment to name of current git branch if not specified
ENVIRONMENT?=$(shell git rev-parse --abbrev-ref HEAD)

test-unit: ## run unit tests
	python3 -m pytest --cov-report html --cov=cezdistribuce ./cezdistribuce/test

run: ## run locally
	func --version
	cd __app__ && func start

security: ## run security check (requires bandit installed)
	bandit --version
	bandit -r ./
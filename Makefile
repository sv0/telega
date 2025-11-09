HOST:=127.0.0.1
PORT:=8000
DEVEL_BRANCH=devel
DOCKER_TAG?=ghcr.io/sv0/telega

.PHONY: help
# target: help - Display callable targets
help:
	@grep -E "^# target:" [Mm]akefile | sed 's/# target: //g'


# https://github.com/sio/Makefile.venv
# Seamlessly manage Python virtual environment with a Makefile
Makefile.venv:
	curl \
		-o Makefile.fetched \
		-L "https://github.com/sio/Makefile.venv/raw/v2023.04.17/Makefile.venv"
	echo "fb48375ed1fd19e41e0cdcf51a4a0c6d1010dfe03b672ffc4c26a91878544f82 *Makefile.fetched" \
		| sha256sum --check - \
		&& mv Makefile.fetched Makefile.venv

include Makefile.venv


.PHONY: install
# target: install - Install pip requirements
install: Makefile.venv $(VENV)
	$(VENV)/pip install \
		--quiet \
		--requirement requirements.txt

.PHONY: clean
# target: clean - Clean repo
clean:
	@rm -rf build dist docs/_build
	find $(CURDIR) -name "*.pyc" -delete
	find $(CURDIR) -name "*.orig" -delete
	find $(CURDIR) -name "__pycache__" | xargs rm -rf

# ==============
#  Bump version
# ==============

.PHONY: release
VERSION?=minor
# target: release - Bump version
release:
	$(VENV)/pip install bumpversion
	$(VENV)/bumpversion $(VERSION)
	@git checkout master
	@git merge $(DEVEL_BRANCH)
	@git checkout $(DEVEL_BRANCH)
	@git push --all
	@git push --tags

.PHONY: minor
minor: release

.PHONY: patch
patch:
	make release VERSION=patch

.PHONY: major
major:
	make release VERSION=major

# ===========
# Development
# ===========

.PHONY: test
# target: test - Runs tests with pytest
test:
	@$(VENV)/pytest

.PHONY: cov
# target: cov - short alias for `coverage`
cov: coverage

.PHONY: coverage
# target: coverage - create test coverage report
coverage:
	$(VENV)/coverage run \
		--source=telega \
		-m pytest
	$(VENV)/coverage report


.PHONY: run
run:
	DEBUG=$(DEBUG)
		$(VENV)/uvicorn telega.app:app --host ${HOST} --port ${PORT}

.PHONY: login
# target: login - Log into telegram account and create session file.
login:
	$(VENV)/python3 login.py

.PHONY: bak
# target: bak - Create session backup
bak:
	gzip --best --stdout *.session > session-backup-$(shell date +%Y-%m-%d).gz


.PHONY: docker-build
docker-build:
	docker build -t $(DOCKER_TAG):latest \
		-t $(DOCKER_TAG):$(shell date +%Y%m%d) .

.PHONY: docker-run
docker-run:
	docker run -ti -p 8000:8000 $(DOCKER_TAG):latest

.PHONY: docker-push
docker-push:
	docker push --all-tags $(DOCKER_TAG)

.PHONY: docker-clean
docker-clean:
	docker images | grep -E "$(DOCKER_TAG)|<none>" | awk '{print $$3}' | xargs docker rmi -f

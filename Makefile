.PHONY: help install clean test run
include .env
export

VENV_NAME?=venv
PYTHON=${VENV_NAME}/bin/python3
.RECIPEPREFIX +=

.DEFAULT: help
help:
	@echo "make install"
	@echo "       install dependencies"
	@echo "make test"
	@echo "       run test script"
	@echo "make run DIR={songs directory}"
	@echo "       run song labeler on songs in DIR"
	@echo "make clean"
	@echo "       clean up directory"

install:
	python3 -m pip install virtualenv
	$(MAKE) venv

# change in requirements.txt -> re-run installation of dependencies.
venv: $(VENV_NAME)/bin/activate
$(VENV_NAME)/bin/activate: requirements.txt
	test -d venv || virtualenv venv
	. venv/bin/activate; ${PYTHON} -m pip install -Ur requirements.txt
	touch venv/bin/activate

run:
	${PYTHON} -m shell $(DIR)

test: venv
	${PYTHON} -m test

clean:
	rm -rf __pycache__


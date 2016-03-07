all:
	@echo "make venv"

venv:
	virtualenv --no-site-package venv
	source ./venv/bin/activate && pip3 install -r requirements.txt

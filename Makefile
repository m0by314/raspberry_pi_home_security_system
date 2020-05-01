.PHONY: help prepare-env test lint install

.DEFAULT: help

CURPWD  := $(shell pwd)

SERVICE:= $(CURPWD)/etc/motion-detector
LINK := /etc/systemd/system/${SERVICE}.service

SHELL := /bin/bash

VENV_NAME?=venv
VENV_ACTIVATE=. $(VENV_NAME)/bin/activate
PYTHON=${VENV_NAME}/bin/python3

help:
	@echo "make prepare-env"; \
    echo "       prepare virtual environment, use only once"; \
    echo "make test"; \
    echo "       run tests"; \
    echo "make lint"; \
    echo "       run pylint"; \
    echo "make install"; \
    echo "       install software"; \

install: install-deps build-service
	echo "Welcome, the installation of the detection system will settle"; \

build_service:
	eval echo $(cat ${SERVICE}.template) > ${SERVICE}.service; \
	if test ! -L ${LINK}; then; \
		ln -s ${SERVICE}.service ${LINK}; \
	fi; \
	systemctl enable ${LINK}; \
	systemctl start ${LINK}; \

prepare-env:
	sudo apt-get -y install python python3-pip
	python3 -m pip install virtualenv
	make venv


venv: $(VENV_NAME)/bin/activate
$(VENV_NAME)/bin/activate:
	test -d $(VENV_NAME) || virtualenv -p python3 $(VENV_NAME)
	${PYTHON} -m pip install -U pip
	${PYTHON} -m pip install -e .
	. venv/bin/activate
	touch $(VENV_NAME)/bin/activate

install-deps: venv
	apt-get install gpac; \
	pip install -r requirements.txt

test: venv
	${PYTHON} -m pytest

lint: venv
	${PYTHON} -m pylint *





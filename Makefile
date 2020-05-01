.PHONY: help test lint install

.DEFAULT: help

CURPWD  := $(shell pwd)

SERVICE:= $(CURPWD)/etc/motion-detector
LINK := /etc/systemd/system/${SERVICE}.service

SHELL := /bin/bash

help:
	@echo "make prepare"; \
    echo "       prepare virtual environment, use only once"; \
    echo "make test"; \
    echo "       run tests"; \
    echo "make lint"; \
    echo "       run pylint"; \
    echo "make install"; \
    echo "       install software"; \

install: prepare build-service
	echo "Welcome, the installation of the detection system will settle"; \

build_service:
	eval echo $(cat ${SERVICE}.template) > ${SERVICE}.service; \
	if test ! -L ${LINK}; then; \
		ln -s ${SERVICE}.service ${LINK}; \
	fi; \
	systemctl enable ${LINK}; \
	systemctl start ${LINK}; \

prepare:
	sudo apt-get -y install python python3-pip gpac; \
	pip install -r requirements.txt; \

test:
	${PYTHON} -m pytest

pylint:
	${PYTHON} -m pylint *





.PHONY: help test install clean

.DEFAULT: help

CURPWD  := $(shell pwd)

SERVICE_NAME := home-surveillance-system.service

SERVICE := etc/${SERVICE_NAME}
SERVICE_TEMPLATE = etc/${SERVICE_NAME}.template

SERVICE_ABSPATH = ${CURPWD}/${SERVICE}
LINK_PATH = /etc/systemd/system/${SERVICE_NAME}

SHELL := /bin/bash

help:
	@echo "make install"; \
    echo "       Start the installation"; \
    echo "make test"; \
    echo "       run tests"; \
    echo "make help"; \
    echo "       show the help"; \
    echo "make clean"; \
    echo "       uninstall"; \

start:
	@echo "-------------------------------------------------"; \
	echo "--- Welcome, the installation has been started ---"; \
	@echo "-------------------------------------------------"; \

install: start install-deps build-service

build-service:
	@echo "build the service"
	eval echo -e $$(cat ${SERVICE_TEMPLATE}) > ${SERVICE}; \
	if test ! -L ${LINK_PATH}; then \
		 sudo ln -s ${SERVICE_ABSPATH} ${LINK_PATH}; \
	fi; \
	sudo systemctl enable ${LINK_PATH}; \
	sudo systemctl start ${LINK_PATH}; \

install-deps:
	@echo "Installation of the dependencies"
	sudo apt-get -y install python3 python3-pip gpac; \
	pip3 install -r requirements.txt; \

test:
	${PYTHON} -m pytest

clean: cleandeps
	@-echo "-----------------"; \
	echo "--- Uninstall ---"; \
	@echo "-----------------"; \
	sudo systemctl disable ${LINK_PATH}; \
	sudo systemctl stop ${LINK_PATH}; \
	sudo rm ${LINK_PATH} ${SERVICE}; \

clean-deps:
	@sudo apt-get -y remove gpac; \
	pip3 uninstall -y  -r requirements.txt ; \

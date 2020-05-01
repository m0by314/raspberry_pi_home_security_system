.PHONY: help test install uninstall

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
    echo "make uninstall"; \
    echo "       uninstall"; \

text-install:
	@echo "-------------------------------------------------"; \
	echo "    Welcome, the installation has been started    "; \
	echo "-------------------------------------------------"; \
	echo ""; \
	echo ""; \

install: text-install install-deps build-service

build-service:
	@echo "Build the service"; \
	echo ""; \
	eval echo -e $$(cat ${SERVICE_TEMPLATE}) > ${SERVICE}; \
	if test ! -L ${LINK_PATH}; then \
		 sudo ln -s ${SERVICE_ABSPATH} ${LINK_PATH}; \
	fi; \
	sudo systemctl enable ${LINK_PATH}; \
	sudo systemctl start ${LINK_PATH}; \

install-deps:
	@echo "Installation of the dependencies"; \
	echo ""; \
	sudo apt-get -y install python3 python3-pip gpac; \
	pip3 install -r requirements.txt; \

test:
	${PYTHON} -m pytest

clean: clean-deps
	@-echo "Remove service"; \
	echo ""; \
	sudo systemctl disable ${LINK_PATH}; \
	sudo systemctl stop ${LINK_PATH}; \
	sudo rm ${LINK_PATH} ${SERVICE}; \

clean-deps:
	@echo "Remove packages"; \
	echo ""; \
	sudo apt-get -y remove gpac; \
	pip3 uninstall -y  -r requirements.txt ; \

uninstall:text-uninstall clean

text-uninstall:
	@echo "-----------------"; \
	echo "    Uninstall    "; \
	echo "-----------------"; \
	echo ""; \
	echo "";
.PHONY: help test install uninstall

.DEFAULT: help

CURPWD  := $(shell pwd)

SERVICE_NAME := home-surveillance-system.service

SERVICE := etc/${SERVICE_NAME}
SERVICE_TEMPLATE = etc/${SERVICE_NAME}.template

SERVICE_ABSPATH = ${CURPWD}/${SERVICE}
LINK_PATH = /etc/systemd/system/${SERVICE_NAME}
DATA = testsuite/data.raw

TOKEN_ID=$$(grep TOKEN_ID config.py | awk ' {print $$3}')

SHELL := /bin/bash

help:
	@echo -e "Usage :"; \
	echo -e "\tmake install     : Start the installation"; \
    echo -e "\tmake test        : Run tests"; \
    echo -e "\tmake help        : Show the help"; \
    echo -e "\tmake uninstall   : Uninstall"; \

text-install:
	@echo "-------------------------------------------------"; \
	echo "    Welcome, the installation has been started    "; \
	echo "-------------------------------------------------"; \


install: text-install check_token_id install-deps build-service test

build-service:
	@echo -e "\n--- Build the service ---\n"; \
	eval echo -e $$(cat ${SERVICE_TEMPLATE}) > ${SERVICE}; \
	if test ! -L ${LINK_PATH}; then \
		 sudo ln -s ${SERVICE_ABSPATH} ${LINK_PATH}; \
	fi; \
	echo -e "--- Activate service ---"; \
	sudo systemctl start ${SERVICE_NAME}; \
	sudo systemctl enable ${LINK_PATH}; \
	echo -e "--- Done ---\n"; \
	echo -e "--- Build service done ---\n"; \

install-deps:
	@echo -e "\n--- Packages installation ---\n"; \
	sudo apt-get -y install python3 python3-pip gpac; \
	echo -e "\n --- Requirements installation ---\n"; \
	pip3 install -r requirements.txt; \

check_token_id:
	@if test ${TOKEN_ID}x = "Your token_id"x; then \
	  	echo "Your token_id isn't define in lib/config"; \
	  	echo "Please set your token_id before launch install"; \
	  	exit; \
	fi; \

test:
	@echo -e "--- Testing ---\n"; \
	sudo systemctl stop ${SERVICE_NAME}; \
	python3 -m unittest testsuite/*_test.py; \
	sudo systemctl start ${SERVICE_NAME}; \

clean: clean-deps
	@-echo -e "\n--- Remove service --- "; \
	sudo systemctl stop ${SERVICE_NAME}; \
	sudo systemctl disable ${LINK_PATH}; \
	sudo rm ${LINK_PATH} ${SERVICE} ${DATA}; \
	echo -e "--- done --\n "; \

clean-deps:
	@echo -e "\n--- Remove packages ---\n"; \
	sudo apt-get -y remove gpac; \
	echo -e "\n--- Remove requirements ---\n"; \
	pip3 uninstall -y  -r requirements.txt ; \

uninstall:text-uninstall clean

text-uninstall:
	@echo "-----------------"; \
	echo "    Uninstall    "; \
	echo "-----------------"; \


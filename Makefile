.PHONY: help test install uninstall

.DEFAULT: help

CURPWD := $(shell pwd)

SERVICE_NAME        = home-security-system.service
SERVICE_TEMPLATE    := ${CURPWD}/templates/${SERVICE_NAME}.template
SERVICE             = /usr/lib/systemd/system/${SERVICE_NAME}
LINK_PATH           = /etc/systemd/system/${SERVICE_NAME}

TOKEN_ID            := $(shell grep TOKEN_ID config.py | awk ' {print $$3" "$$4}')
DATA                = testsuite/data.raw

SHELL               := /bin/bash

help:
	@echo -e "Usage :"; \
	echo -e "\tmake install     : Start the installation"; \
    echo -e "\tmake test        : Run tests"; \
    echo -e "\tmake help        : Show the help"; \
    echo -e "\tmake uninstall   : Uninstall"; \

text-install:
	@echo "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"; \
	echo "@@@   Welcome, the installation has been started   @@@"; \
	echo "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"; \


install: text-install check_token_id install-deps build-service set-up-camera reboot

set-up-camera:
	@raspi-config nonint do_camera 0; \

set-down-camera:
	@raspi-config nonint do_camera 1; \

reboot:
	@echo "Reboot necessary to finish"; \
	echo "The raspberry will reboot in 10 seconds"; \
	shutdown -r -t 10; \

build-service:
	@echo "-------------------------"; \
	echo "---   Build service   ---"; \
	echo "-------------------------"; \
	eval echo -e $$(cat ${SERVICE_TEMPLATE}) > ${SERVICE}; \
	if test ! -L ${LINK_PATH}; then \
		 ln -s ${SERVICE} ${LINK_PATH}; \
	fi; \
	systemctl start ${SERVICE_NAME}; \
	systemctl enable ${SERVICE_NAME}; \
	echo -e "--- Done ---\n"; \

install-deps:
	@echo "------------------------"; \
	echo "---   Requirements   ---"; \
	echo "------------------------"; \
	apt-get -y update; \
	apt-get -y install python3 python3-pip gpac; \
	pip3 install -r requirements.txt; \
	echo -e "--- Done ---\n"; \

check_token_id:
	@if [ "${TOKEN_ID}"x == "'Your token_id'"x ]; then \
		echo ""; \
                echo "Your token_id isn't define in config.py"; \
                echo "Please set your token_id"; \
		echo ""; \
                exit 1; \
        fi; \

test: check_token_id
	@echo "-------------------"; \
	echo "---   Testing   ---"; \
	echo "-------------------"; \
	sudo systemctl stop ${SERVICE_NAME}; \
	python3 -m unittest testsuite/*_test.py; \
	sudo systemctl start ${SERVICE_NAME}; \

clean: clean-deps
	@echo -e "\n--- Remove service --- "; \
	systemctl stop ${SERVICE_NAME}; \
	systemctl disable ${SERVICE_NAME}; \
	rm ${LINK_PATH} ${SERVICE} ${DATA}; \
	echo -e "--- Done --\n "; \

clean-deps:
	@sudo apt-get -y remove gpac; \
	pip3 uninstall -y  -r requirements.txt ; \
	echo -e "\n--- Done ---\n"; \

uninstall:text-uninstall clean set-down-camera reboot

text-uninstall:
	@echo "---------------------"; \
	echo "---   Uninstall   ---"; \
	echo "---------------------"; \


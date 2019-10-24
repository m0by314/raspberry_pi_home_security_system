#!/usr/bin/env python3
# installation script 

import subprocess
import os
import sys

from bin.sed import sed

print('Welcome, the installation of the detection system will settle')

if 'SUDO_USER' in os.environ:
    user = os.environ['SUDO_USER']
else:
    sys.exit('The setup script has not launch with sudo command')

current_dir = os.getcwd()
prog = 'osiris.py'
template = 'etc/osiris.service'
service_name = 'osiris.service'
service = '/etc/systemd/system/' + service_name
link = current_dir + '/' + template

properties = {'^ExecStart=.*': 'ExecStart=' + current_dir + '/bin/' + prog,
              '^WorkingDirectory=.*': 'WorkingDirectory=' + current_dir,
              '^User=.*': 'User=' + user
              }

cmd = {"enable": {'args': ["systemctl", "enable", service_name],
                  'err': 'Error during enable service'
                  },
       "start": {'args': ["systemctl", "start", service_name],
                 'err': 'Error during start service'
                 },
       "status": {'args': ["systemctl", "status", service_name],
                  'err': 'Error during status service'
                  },
       }


def build_service():
    for key in properties.keys():
        if sed(template, key, properties[key]) != 0:
            raise Exception('Error during sed in' + template)


def linked():
    if os.path.islink(service):
        os.unlink(service)
    os.symlink(link, service)


def activate_service():
    for k in cmd.keys():
        process = subprocess.run(cmd[k]['args'])
        if process.returncode != 0:
            raise Exception(cmd[k]['err'])


def main():
    build_service()
    linked()
    activate_service()


if __name__ == '__main__':
    main()

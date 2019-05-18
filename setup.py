#!/usr/bin/env python3
# installation script 

import subprocess
import os
import sys
import getpass
from lib.sed import sed


print('Welcome, the installation of the detection system will settle')

if 'SUDO_USER' in os.environ:
    user = os.environ['SUDO_USER']
else:
    sys.exit('The setup script has not launch with sudo command')

current_dir         = os.getcwd()
script_name         = 'osiris.py'
local_service_path  = 'etc/osiris.service'
service_name        = 'osiris.service'
service_path        = '/etc/systemd/system/' + service_name
link_path           = current_dir + '/' + local_service_path

properties = { '^ExecStart=.*'         : 'ExecStart=' + current_dir + '/' + script_name,
                '^WorkingDirectory=.*' : 'WorkingDirectory=' + current_dir,
                '^User=.*'             : 'User=' + user
            }

cmd = { "enable" : { 'args' : ["systemctl", "enable", service_name],
                     'err'  : 'Error during enable service'
                     },
        "start"  : { 'args' : ["systemctl", "start", service_name],
                     'err'  : 'Error during start service'
                    },
       "status"  : { 'args' : ["systemctl", "status", service_name],
                     'err'  : 'Error during status service'
                    },
    }

def build_service():
  for key in properties.keys():
      if sed(local_service_path,key,properties[key]) != 0 :
         raise Exception('Error during sed in' + local_service_path )

def link():
  if os.path.islink(service_path):
      os.unlink(service_path)  
  os.symlink(link_path, service_path)

def activate_service():
  for k in cmd.keys():
      process = subprocess.run(cmd[k]['args'])
      if process.returncode != 0:
         raise Exception(cmd[k]['err'])
          
def main():
  build_service()
  link()
  activate_service()
  
  
if __name__ == '__main__':
   main()
    

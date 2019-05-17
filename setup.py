#! /usr/bin/python3
# installation script 

import subprocess
import os
import getpass
from lib.sed import sed


print('Welcome, the installation of the detection system will settle')


current_dir         = os.getcwd()
current_user        = getpass.getuser()
local_service_path  = 'etc/motion.service'
link_path           = current_dir + '/' + local_service_path
service_name        = 'motion.service'
service_path        = '/etc/systemd/system/' + service_name

properties = { '^ExecStart=.*'         : 'ExecStart=' + current_dir + '/motion.py',
                '^WorkingDirectory=.*' : 'WorkingDirectory=' + current_dir,
                '^User=.*'             : 'User=' + current_user
            }

cmd = { "enable" : { 'args' : ["systemctl", "enable", service_name],
                     'err'  : 'Error during enable service'
                     },
        "start"  : { 'args' : ["systemctl", "start", service_name],
                     'err'  : 'Error during start service'
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
    

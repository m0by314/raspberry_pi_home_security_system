#! /usr/bin/python3
# installation script 
import subprocess
import os
from lib.sed import sed

#TODO format presentation
print('Welcome, the installation of the detection system will settle')


current_dir = os.getcwd()
current_user = os.getusername()


local_service_path = 'etc/motion.service'
link_path = current_dir + '/' + local_service_path
service_name = 'motion.service'
service_path = '/etc/systemd/system/' + service_name

properties = { '^ExecStart'         : ExecStart = 'ExecStart=' + current_dir + '/bin/motion.py',
                '^WorkingDirectory' : WorkingDirectory = 'WorkingDirectory=' + current_dir,
                '^User'             : User = 'User=' + current_user
              }

#$ExecStart = 'ExecStart=' + $current_dir = 'bin/motion.py'
#$WorkingDirectory = 'WorkingDirectory=' + $current_dir
#$User = 'User=' + $current_user

#sed($service, '^ExecStart', $ExecStart)
#sed($service, '^WorkingDirectory', $WorkingDirectory)
#sed($service, '^User', $User)

for key in properties.keys():
    sed(local_service_path,key,properties[key])


os.symlink(link_path, service_path)

cmd = subprocess.run(["systemctl", "enable", service_name], capture_output=True)
if cmd.returncode != 0:
    raise Exception('Error during enable service')
    
cmd = subprocess.run(["systemctl", "start", service_name], capture_output=True)
if cmd.returncode != 0:
    raise Exception('Error during start service')    

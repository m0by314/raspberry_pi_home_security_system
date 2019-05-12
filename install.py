#! /usr/bin/python3
# installation script 
import sys
import fileinput

#TODO format presentation
print('Welcome, the installation of the detection system will settle')
print('Requirement : You need your token ID before installation')



def yes_or_no(question):
    while "the answer is invalid":
        reply = str(input(question+' (y/n): ')).lower().strip()
        if reply[:1] == 'y':
            return True
        if reply[:1] == 'n':
            return False
        else:
            print("the answer is invalid")

# TODO sed fonction 
def sed(file):
    for line in fileinput.input(file, inplace=True):
    # inside this loop the STDOUT will be redirected to the file
    # the comma after each print statement is needed to avoid double line breaks
    print(line.replace("hello", "helloworld"))
    
    
# Start :
if not (yes_or_no('Start installation ?')):
    print('exit')
    sys.exit(1)

token = input('Enter your token id:')
print("local.py configuration")

# TODO Modifier le fichier service 
# creation du lien et activation 
# 
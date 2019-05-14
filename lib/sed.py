#!/usr/bin/python3

import re
import sys
import shutil

def sed(file,motif,remplacement):
        regex = re.compile(motif)
        tmpfile = file + '.tmp'
 
        fin = open(file,'r')
        fout = open(tmpfile,'w')
        
        sys.stdout = fout   # Change STDOUT channel
        
        for line in fin:
                if (regex.match(line)):
                        line = re.sub(motif,remplacement,line)
                        sys.stdout.write(str(line))
                else:
                        sys.stdout.write(str(line))
        fin.close()
        fout.close()
        
        shutil.move(tmpfile,file)

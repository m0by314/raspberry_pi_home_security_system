#!/usr/bin/python3

import re
import sys
import shutil

def sed(file,motif,remplacement):
        regex = re.compile(motif)
        tmpfile = file + '.tmp'
        err = 0
 
        fin = open(file,'r')
        fout = open(tmpfile,'w')
        
        sys.stdout = fout   # Change STDOUT channel
        
        for line in fin:
            line = re.sub(motif,remplacement,line)
            try :
                sys.stdout.write(str(line))
            except Exception as E :
                raise E
                err = 1
        
        fin.close()
        fout.close()
        
        if ( err != 1 ) :
            shutil.move(tmpfile,file)
        
        
if __name__ == '__main__':
    if (len(sys.argv) != 4):
        print('Usage:')
        print('\t' + sys.argv[0] + ' file motif remplacement')
    else:   
        sed(sys.argv[1],sys.argv[2],sys.argv[3])

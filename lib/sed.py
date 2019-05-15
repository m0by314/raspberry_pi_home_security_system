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
                return err
        
        fin.close()
        fout.close()
        
        if ( err != 1 ) :
            shutil.move(tmpfile,file)
    
        return  err    
        

#!/usr/bin/env python
from protagonist import tagger
import os, sys

cwd = os.getcwd()
t = tagger.Tagger(cwd)
bool_list = sys.argv[1:]
for f in t.get_names(t.parse(bool_list)):
    sys.stdout.write(f + "\n")
    
    

    



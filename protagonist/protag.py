#!/usr/bin/env python
from protagonist import tagger
import os, sys

cwd = os.getcwd()
t = tagger.Tagger(cwd)

if sys.argv[1] == "ls":
    bool_list = sys.argv[2:]
    for f in t.get_names(t.parse(bool_list)):
        sys.stdout.write(f + "\n")
elif sys.argv[1] == "add":
    file_name = sys.argv[2]
    tags = sys.argv[3:]
    for tag in tags:
        t.tag_file(file_name, tag)
    

    



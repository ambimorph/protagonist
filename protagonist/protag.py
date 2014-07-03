#!/usr/bin/env python
from protagonist import tagger
import os, sys, shutil

def main():

    cwd = os.getcwd()
    t = tagger.Tagger(cwd)

    if sys.argv[1] == "ls":
        bool_list = sys.argv[2:]
        for f in t.get_names(t.parse(bool_list)):
            sys.stdout.write(f + "\n")
    elif sys.argv[1] == "tag":
        file_name = sys.argv[2]
        tags = sys.argv[3:]
        for tag in tags:
            t.tag_file(file_name, tag)
    elif sys.argv[1] == "untag":
        file_name = sys.argv[2]
        tags = sys.argv[3:]
        for tag in tags:
            t.untag_file(file_name, tag)
    elif sys.argv[1] == "rmtag":
        tag = sys.argv[2]
        t.delete_tag(tag)
    elif sys.argv[1] == "rm":
        file_name = os.path.abspath(sys.argv[2])
        t.rm_file(file_name)
        os.remove(file_name)
    elif sys.argv[1] == "mv":
        file_name = sys.argv[2]
        new_name = sys.argv[3]
        shutil.copy(file_name, new_name)
        t.mv_file(file_name, new_name)
        os.remove(file_name)

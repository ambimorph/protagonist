#!/usr/bin/env python
from protagonist import tagger, __version__
import argparse, os, sys, shutil

def main():

    cwd = os.getcwd()
    t = tagger.Tagger(cwd)

    def ls(args):
        for f in t.get_names(t.parse(args.expr)):
            sys.stdout.write(f + "\n")

    def tag(args):
        file_name = args.file_name
        for tag in args.tags:
            t.tag_file(file_name, tag)

    def untag(args):
        file_name = args.file_name
        for tag in args.tags:
            t.untag_file(file_name, tag)

    def rmtag(args):
        for tag in args.tags:
            t.delete_tag(tag)

    def rm(args):
        for f in args.file_names:
            t.rm_file(f)
            os.remove(f)

    def mv(args):
        file_name = args.old
        new_name = args.new
        shutil.copy(file_name, new_name)
        t.mv_file(file_name, new_name)
        os.remove(file_name)

    parser = argparse.ArgumentParser(description='Tagsystem operations.')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)
    subparsers = parser.add_subparsers(help='sub-command help')

    parser_ls = subparsers.add_parser('ls', help='list files with a Bool tag expression')
    parser_ls.add_argument('expr', metavar='Boolean tag expression', type=str, nargs='+')
    parser_ls.set_defaults(func=ls)

    parser_tag = subparsers.add_parser('tag', help='tag a file with tags')
    parser_tag.add_argument('file_name', metavar='filename', type=str)
    parser_tag.add_argument('tags', metavar='tag', type=str, nargs='+')
    parser_tag.set_defaults(func=tag)

    parser_untag = subparsers.add_parser('untag', help='untag a file from tags')
    parser_untag.add_argument('file_name', metavar='filename', type=str)
    parser_untag.add_argument('tags', metavar='tag', type=str, nargs='+')
    parser_untag.set_defaults(func=untag)

    parser_rmtag = subparsers.add_parser('rmtag', help='remove tags from system.')
    parser_rmtag.add_argument('tags', metavar='tag', type=str, nargs='+')
    parser_rmtag.set_defaults(func=rmtag)

    parser_rm = subparsers.add_parser('rm', help='consistently remove files from underlying FS')
    parser_rm.add_argument('file_names', metavar='filename', type=str, nargs='+')
    parser_rm.set_defaults(func=rm)

    parser_mv = subparsers.add_parser('mv', help='consistently mv file in underlying FS')
    parser_mv.add_argument('old', metavar='old', type=str)
    parser_mv.add_argument('new', metavar='new', type=str)
    parser_mv.set_defaults(func=mv)


    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()

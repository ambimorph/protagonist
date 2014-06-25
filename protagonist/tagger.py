import os
from pyblake2 import blake2b

class Tagger():

    def __init__(self, base_directory):

        self.dict_directory = base_directory + "/.protagonist/"
        self.tag_directory = self.dict_directory + "tags/"

    def create_tagsystem(self):

        try:
            os.mkdir(self.dict_directory)
            os.mkdir(self.tag_directory)
        except OSError, e:
            pass

    def add_tag(self, tag):

        try:
            os.mkdir(self.tag_directory + tag + "/")
        except OSError, e:
            pass

    def make_file_id(self, file_name):

        extension = os.path.splitext(file_name)[1]
        contents = open(file_name, 'r').read()
        blake2hash = blake2b(contents, digest_size=20).hexdigest()
        return blake2hash + extension

    def tag_file(self, file_name, tag):

        self.add_tag(tag)
        file_id = self.make_file_id(file_name)
        os.link(file_name, self.tag_directory + tag + "/" + file_id)

    def get_inode(self, file_name):
        return os.stat(file_name).st_ino

    def untag_file(self, file_name, tag):

        tagged_file_path = self.tag_directory + tag + "/" + self.make_file_id(file_name)

        # Assert a copy of the file is tagged with tag
        try:
            assert os.path.exists(tagged_file_path)
        except AssertionError, e:
            return (False, file_name + " is not tagged with " + tag + "!\n")

        # Assert the tagged copy is this copy
        try:
            assert os.stat(file_name).st_ino == os.stat(tagged_file_path).st_ino
        except AssertionError, e:
            return (False, file_name + " is not tagged with " + tag + " (but a copy is)!\n")
        os.remove(tagged_file_path)

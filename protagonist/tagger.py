import os, shutil
from pyblake2 import blake2b

class Tagger():

    def __init__(self, base_directory=os.getcwd()):

        self.dict_directory = os.path.abspath(os.path.join(base_directory, ".protagonist"))
        self.tag_directory = os.path.join(self.dict_directory, "tags")
        self.truenames_directory = os.path.join(self.dict_directory, "truenames")
        self.create_tagsystem()

    def create_tagsystem(self):

        try:
            os.mkdir(self.dict_directory)
            os.mkdir(self.tag_directory)
            os.mkdir(self.truenames_directory)
        except OSError, e:
            pass

    def add_tag(self, tag):

        try:
            os.mkdir(os.path.join(self.tag_directory, tag))
        except OSError, e:
            pass

    def make_file_id(self, file_name):

        extension = os.path.splitext(file_name)[1]
        with open(file_name, 'r') as f:
            contents = f.read()
        blake2hash = blake2b(contents, digest_size=20).hexdigest()
        return blake2hash + extension

    def tag_file(self, file_name, tag):

        self.add_tag(tag)
        file_id = self.make_file_id(file_name)
        os.link(file_name, os.path.join(self.tag_directory, tag, file_id))
        with open(os.path.join(self.truenames_directory, file_id), 'w') as f:
            f.write(os.path.abspath(file_name))

    def get_inode(self, file_name):
        return os.stat(file_name).st_ino

    def untag_file(self, file_name, tag):

        tagged_file_path = os.path.join(self.tag_directory, tag, self.make_file_id(file_name))

        # Assert a copy of the file is tagged with tag
        try:
            assert os.path.exists(tagged_file_path)
        except AssertionError, e:
            raise TaggerException(file_name + " is not tagged with " + tag + "!\n")

        # Assert the tagged copy is this copy
        try:
            assert os.stat(file_name).st_ino == os.stat(tagged_file_path).st_ino
        except AssertionError, e:
            raise TaggerException(file_name + " is not tagged with " + tag + " (but a copy is)!\n")
        os.remove(tagged_file_path)

        # If the tag directory is now empty, remove it.
        if os.listdir(os.path.join(self.tag_directory, tag)) == []:
            os.rmdir(os.path.join(self.tag_directory, tag))

    def delete_tag(self, tag):

        try:
            shutil.rmtree(os.path.join(self.tag_directory, tag))
        except OSError, e:
            pass

    def tag_ls(self, tag):
        """
        Returns the set of file IDs that match a given tag.
        """

        this_tag_path = os.path.join(self.tag_directory, tag)
        if os.path.exists(this_tag_path):
            return set(os.listdir(this_tag_path))
        else:
            return set([])

    def get_names(self, file_set):

        def name(file_id):
            with open(os.path.join(self.truenames_directory, file_id), 'r') as f:
                return f.read()

        return map(name, file_set)
            
class TaggerException(Exception):
    pass

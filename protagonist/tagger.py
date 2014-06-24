import os

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


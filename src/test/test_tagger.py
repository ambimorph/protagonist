import unittest, tagger, os


class TaggerTest(unittest.TestCase):

    def setUp(self):
        
        tagger.create_tagsystem({"base_directory" : "/tmp/.protagonist"})
        self.tag_0 = "test_tag_0"
        self.tag_1 = "test_tag_1"
        self.tag_2 = "test_tag_2"
        self.file_name_0 = "test_file_name_0"
        self.file_name_1 = "test_file_name_1"
        self.file_name_2 = "test_file_name_2"
        open(self.file_name_0, 'w').close()
        open(self.file_name_1, 'w').close()
        open(self.file_name_2, 'w').close()

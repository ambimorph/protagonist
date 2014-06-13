from protagonist import tagger
import unittest, os


class TaggerTest(unittest.TestCase):

    def setUp(self):

        tagger.create_tagsystem({"base_directory" : "/tmp/.protagonist"})

        self.test_tags = ["test_tag_" + str(i) for i in range(2)]
        self.file_names = ["file_name_" + str(i) for i in range(2)]

        def touch(file_name):
            open(file_name, 'w').close()

        map(touch, self.file_names)

if __name__ == '__main__':
    unittest.main()

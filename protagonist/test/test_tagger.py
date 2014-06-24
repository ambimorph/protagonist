from protagonist import tagger
import unittest, os, shutil


class TaggerTest(unittest.TestCase):

    def setUp(self):

        # Guarantee we can make a fresh directory somewhere
        found_unique_directory_name = False
        suffix = 0
        while not found_unique_directory_name:
            try:
                self.sandbox = "/tmp/tagger_test" + str(suffix) + "/"
                os.mkdir(self.sandbox)
                found_unique_directory_name = True
            except OSError, e:
                suffix += 1

        # Now setup for real
        self.tagger = tagger.Tagger(self.sandbox)
        self.tagger.create_tagsystem()

        self.test_tags = ["test_tag_" + str(i) for i in range(2)]
        self.file_names = [self.sandbox + "file_name_" + str(i) for i in range(2)]

        def touch(file_name):
            open(file_name, 'w').close()

        map(touch, self.file_names)

    def test_create_tagsystem(self):

        self.assertTrue(os.path.exists(self.tagger.tag_directory))

        # Also check for idempotence
        self.tagger.create_tagsystem()
        self.assertTrue(os.path.exists(self.tagger.tag_directory))

    def test_add_tag(self):

        map(self.tagger.add_tag, self.test_tags)
        expected_directories = [self.tagger.tag_directory + "/" + t for t in self.test_tags]
        for directory in expected_directories:
            self.assertTrue(os.path.exists(directory))

        # Also check for idempotence
        map(self.tagger.add_tag, self.test_tags)
        for directory in expected_directories:
            self.assertTrue(os.path.exists(directory))

    def tearDown(self):

        shutil.rmtree(self.sandbox)

if __name__ == '__main__':
    unittest.main()

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
        self.file_names = [self.sandbox + "file_name_" + str(i) + ".txt" for i in range(2)]

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

    def test_make_file_id(self):

        hellofile = self.sandbox + "hellofile.txt"
        open(hellofile, 'w').write("Hello, world!\n")
        file_id = self.tagger.make_file_id(hellofile)
        self.assertEqual(file_id, "27406a32541c9783e0ce5e47dedab392728565a4.txt"), file_id

    def test_tag_file(self):

        self.tagger.tag_file(self.file_names[0], self.test_tags[0])
        directory_path = self.tagger.tag_directory + "/" +  self.test_tags[0] + "/"
        self.assertTrue(os.path.exists(directory_path + "3345524abf6bbe1809449224b5972c41790b6cf2.txt"), msg = os.listdir(directory_path))

    def tearDown(self):

        shutil.rmtree(self.sandbox)

if __name__ == '__main__':
    unittest.main()

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
        n = 3 # number of files and tags to create for testing

        self.test_tags = ["test_tag_" + str(i) for i in range(n)]
        self.file_names = [self.sandbox + "file_name_" + str(i) + ".txt" for i in range(n)]
        self.file_contents = ["foo", "bar", "baz"]

        def insert_contents(file_name, content_string):
            f = open(file_name,'w')
            f.write(content_string)
            f.close()

        for i in range(3):
            insert_contents(self.file_names[i], self.file_contents[i])

        self.duplicate = os.path.join(self.sandbox, "dup.txt")
        insert_contents(self.duplicate, "foo")

        self.ids = map(self.tagger.make_file_id, self.file_names)

    def test_create_tagsystem(self):

        self.assertTrue(os.path.exists(self.tagger.tags_directory))

        # Also check for idempotence
        self.tagger.create_tagsystem()
        self.assertTrue(os.path.exists(self.tagger.tags_directory))
        self.assertTrue(os.path.exists(self.tagger.truenames_directory))

    def test_add_tag(self):

        map(self.tagger.add_tag, self.test_tags)
        expected_directories = [self.tagger.path_join_tag(t) for t in self.test_tags]
        for directory in expected_directories:
            self.assertTrue(os.path.exists(directory))

        # Also check for idempotence
        map(self.tagger.add_tag, self.test_tags)
        for directory in expected_directories:
            self.assertTrue(os.path.exists(directory))

    def test_make_file_id(self):

        file_id = self.tagger.make_file_id(self.file_names[0])
        self.assertEqual(file_id, "983ceba2afea8694cc933336b27b907f90c53a88.txt"), file_id

    def test_tag_file(self):

        self.tagger.tag_file(self.file_names[0], self.test_tags[0])
        expected_file_id = self.ids[0]
        directory_path = self.tagger.path_join_tag(self.test_tags[0])
        self.assertTrue(os.path.exists(os.path.join(directory_path, expected_file_id)), msg = os.listdir(directory_path))
        self.assertTrue(os.path.exists(self.tagger.path_join_truenames(expected_file_id)), msg = os.listdir(self.tagger.truenames_directory))
        contents = open(self.tagger.path_join_truenames(expected_file_id), 'r').read()
        self.assertEquals(contents, self.file_names[0]), contents

    def test_untag_file(self):

        with self.assertRaises(tagger.TaggerException):
            self.tagger.untag_file(self.file_names[0], self.test_tags[0])

        with self.assertRaises(tagger.TaggerException):
            self.tagger.untag_file(self.duplicate, self.test_tags[0])

        # tag all with tag0, then untag f0.
        for file_name in self.file_names:
            self.tagger.tag_file(file_name, self.test_tags[0])
        directory_path = self.tagger.path_join_tag(self.test_tags[0])
        self.tagger.untag_file(self.file_names[0], self.test_tags[0])

        # make sure f0 is not in the tag0 directory
        self.assertFalse(os.path.exists(directory_path + self.ids[0]), msg = os.listdir(directory_path))

        # make sure that f0 is no longer in truenames
        tags = self.tagger.file_ls_tags(self.file_names[0])
        self.assertSetEqual(tags, set([])), tags
        self.assertFalse(os.path.exists(self.tagger.path_join_truenames(self.ids[0])), msg = os.listdir(self.tagger.truenames_directory))
        # make sure the other files are still in tag0
        for file_id in self.ids[1:]:
            self.assertTrue(os.path.exists(os.path.join(directory_path, file_id)), msg = os.listdir(directory_path))

        # make sure after all files untagged, tag0 dir is removed.
        for i in range(2):
            self.tagger.untag_file(self.file_names[i+1], self.test_tags[0])
        self.assertFalse(os.path.exists(directory_path), msg = os.listdir(self.tagger.tags_directory))

    def test_delete_tag(self):

        directory_path = self.tagger.path_join_tag(self.test_tags[0])
        self.tagger.delete_tag(self.test_tags[0])
        self.assertFalse(os.path.exists(directory_path), msg = os.listdir(self.tagger.tags_directory))
        self.tagger.tag_file(self.file_names[0], self.test_tags[0])
        self.tagger.delete_tag(self.test_tags[0])
        self.assertFalse(os.path.exists(directory_path), msg = os.listdir(self.tagger.tags_directory))
        self.assertFalse(os.path.exists(self.tagger.path_join_truenames(self.ids[0])), msg = os.listdir(self.tagger.truenames_directory))

    def test_tag_ls(self):

        for file_name in self.file_names:
            self.tagger.tag_file(file_name, self.test_tags[0])
        directory_path = self.tagger.path_join_tag(self.test_tags[0])

        tagged = self.tagger.tag_ls(self.test_tags[0])
        self.assertSetEqual(tagged, set(map(self.tagger.make_file_id, self.file_names))), tagged

    def test_file_ls_tags(self):

        for tag in self.test_tags:
            self.tagger.tag_file(self.file_names[0], tag)

        tags = self.tagger.file_ls_tags(self.file_names[0])
        self.assertSetEqual(tags, set(self.test_tags)), tags

        self.tagger.untag_file(self.file_names[0], self.test_tags[0])
        tags = self.tagger.file_ls_tags(self.file_names[0])
        self.assertSetEqual(tags, set(self.test_tags[1:])), tags

    def test_get_names(self):

        for file_name in self.file_names:
            self.tagger.tag_file(file_name, self.test_tags[0])

        ids = map(self.tagger.make_file_id, self.file_names)
        names = self.tagger.get_names(ids)
        self.assertSetEqual(names, set(self.file_names)), names

    def test_rm_file(self):

        self.tagger.tag_file(self.file_names[0], self.test_tags[0])
        self.tagger.rm_file(self.file_names[0])
        tags = self.tagger.file_ls_tags(self.file_names[0])
        self.assertSetEqual(tags, set([])), tags
        self.assertFalse(os.path.exists(self.tagger.path_join_truenames(self.ids[0])), msg = os.listdir(self.tagger.truenames_directory))

    def test_mv_file(self):

        self.tagger.tag_file(self.file_names[0], self.test_tags[0])

        # move it, check the truename is still there, but point
        # differently, and the tags still hold.
        new_name = os.path.join(self.sandbox, "foo.txt")
        shutil.copy(self.file_names[0], new_name)
        self.tagger.mv_file(self.file_names[0], new_name)
        self.assertTrue(os.path.exists(self.tagger.path_join_truenames(self.ids[0])), msg = os.listdir(self.tagger.truenames_directory))
        with open(self.tagger.path_join_truenames(self.ids[0]), 'r') as f:
            path = f.read()
            self.assertEqual(path, new_name), path
        tags = self.tagger.file_ls_tags(new_name)
        self.assertSetEqual(tags, set([self.test_tags[0]])), tags
        # move it again, this time the id needs a new extension
        new_new_name = os.path.join(self.sandbox, "foo.rst")
        shutil.copy(self.file_names[0], new_new_name)
        self.tagger.mv_file(new_name, new_new_name)
        self.assertFalse(os.path.exists(self.tagger.path_join_truenames(self.ids[0])), msg = os.listdir(self.tagger.truenames_directory))
        self.assertTrue(os.path.exists(self.tagger.path_join_truenames(self.tagger.make_file_id(new_new_name))), msg = os.listdir(self.tagger.truenames_directory))

        tags = self.tagger.file_ls_tags(new_name)
        self.assertSetEqual(tags, set([])), tags
        tags = self.tagger.file_ls_tags(new_new_name)
        self.assertSetEqual(tags, set([self.test_tags[0]])), tags

    def test_parse(self):

        for i in range(len(self.file_names)):
            self.tagger.tag_file(self.file_names[i], self.test_tags[i])
        self.tagger.tag_file(self.file_names[0], self.test_tags[1])

        def get_names_matching_bool(expression):
            return self.tagger.get_names(self.tagger.parse(expression))

        # Now all files are tagged with the corresponding tag, and
        # file0 is also tagged with tag1

        # expression is a single term
        result = get_names_matching_bool([self.test_tags[0]])
        self.assertSetEqual(result, set([self.file_names[0]]))

        # expression consists of one AND
        expression = self.test_tags[0] + " AND " + self.test_tags[1]
        result = get_names_matching_bool(expression.split())
        self.assertSetEqual(result, set([self.file_names[0]]))

        expression = self.test_tags[2] + " AND " + self.test_tags[1]
        result = get_names_matching_bool(expression.split())
        self.assertSetEqual(result, set([]))

        # expression consists of one OR
        expression = self.test_tags[2] + " OR " + self.test_tags[1]
        result = get_names_matching_bool(expression.split())
        self.assertSetEqual(result, set(self.file_names))

        # expression consists of one NOT
        expression = "NOT " + self.test_tags[0]
        result = get_names_matching_bool(expression.split())
        self.assertSetEqual(result, set(self.file_names[1:]))

        # More complex expressions with AND, NOT, OR
        expression = self.test_tags[1] + " AND NOT " + self.test_tags[0]
        result = get_names_matching_bool(expression.split())
        self.assertSetEqual(result, set([self.file_names[1]]))

        # This one relies on correct ordering.
        expression = self.test_tags[1] + " OR " + self.test_tags[2] + " AND " + self.test_tags[0]
        result = get_names_matching_bool(expression.split())
        self.assertSetEqual(result, set([self.file_names[0]]))

        # Expressions with parenthesis

        expression = "( " + self.test_tags[0] + " )"
        result = get_names_matching_bool(expression.split())
        self.assertSetEqual(result, set([self.file_names[0]]))

        expression = self.test_tags[1] + " OR " + self.test_tags[2] + " AND " + self.test_tags[0] + " )"
        with self.assertRaises(tagger.TaggerException):
            result = get_names_matching_bool(expression.split())

        expression = self.test_tags[1] + " OR ( " + self.test_tags[2] + " AND " + self.test_tags[0] + " )"
        result = get_names_matching_bool(expression.split())
        self.assertSetEqual(result, set(self.file_names[:2]))

    def tearDown(self):

        shutil.rmtree(self.sandbox)

if __name__ == '__main__':
    unittest.main()

import os, shutil
from pyblake2 import blake2b

class Tagger():

    def __init__(self, base_directory=os.getcwd()):

        self.dict_directory = os.path.abspath(os.path.join(base_directory, ".protagonist"))
        self.tags_directory = os.path.join(self.dict_directory, "tags")
        self.truenames_directory = os.path.join(self.dict_directory, "truenames")
        self.create_tagsystem()
        self.OPS = {
            "AND": (set.intersection, 2),
            "OR": (set.union, 2),
            "NOT": ((lambda x: set.difference(self.universe(), x)), 1)
            }
        self.parentheses = ["(", ")"]

    def path_join_tag(self, *args):
        return os.path.join(self.tags_directory, *args)

    def path_join_truenames(self, *args):
        return os.path.join(self.truenames_directory, *args)

    def universe(self):
        return set(os.listdir(self.truenames_directory))

    def create_tagsystem(self):

        try:
            os.mkdir(self.dict_directory)
            os.mkdir(self.tags_directory)
            os.mkdir(self.truenames_directory)
        except OSError, e:
            pass

    def add_tag(self, tag):

        try:
            os.mkdir(self.path_join_tag(tag))
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
        os.link(file_name, self.path_join_tag(tag, file_id))
        # TODO check if it is there first?
        with open(self.path_join_truenames(file_id), 'w') as f:
            f.write(os.path.abspath(file_name))

    def get_inode(self, file_name):
        return os.stat(file_name).st_ino

    def untag_file(self, file_name, tag):

        tagged_file_path = self.path_join_tag(tag, self.make_file_id(file_name))

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
        if os.listdir(self.path_join_tag(tag)) == []:
            os.rmdir(self.path_join_tag(tag))

        # If the file has no more tags, remove it from truenames
        if self.file_ls_tags(file_name) == set([]):
            os.remove(self.path_join_truenames(self.make_file_id(file_name)))

    def delete_tag(self, tag):

        try:
            path = self.path_join_tag(tag)
            file_names = self.get_names(os.listdir(path))
            for file_name in file_names:
                self.untag_file(file_name, tag)
            os.rmdir(path)
        except OSError, e:
            pass

    def tag_ls(self, tag):
        """
        Returns the set of file IDs that match a given tag.
        """

        this_tag_path = self.path_join_tag(tag)
        if os.path.exists(this_tag_path):
            return set(os.listdir(this_tag_path))
        else:
            return set([])

    def file_ls_tags(self, file_name):

        file_id = self.make_file_id(file_name)
        tag_set = set([])
        for tag_directory in os.listdir(self.tags_directory):
            if os.path.exists(self.path_join_tag(tag_directory, file_id)):
                tag_set.add(os.path.basename(tag_directory))
        return tag_set

    def rm_file(self, file_name):

        for tag in self.file_ls_tags(file_name):
            self.untag_file(file_name, tag)

    def mv_file(self, old_name, new_name):

        new_file_id = self.make_file_id(new_name)
        for tag in self.file_ls_tags(old_name):
            self.untag_file(old_name, tag)
            self.tag_file(new_name, tag)

        with open(self.path_join_truenames(new_file_id), 'w') as f:
            f.write(os.path.abspath(new_name))

    def get_names(self, file_set):

        def name(file_id):
            with open(self.path_join_truenames(file_id), 'r') as f:
                return f.read()

        return set(map(name, file_set))

    def parse(self, bool_list):
        """

        """

        def trace():
            for l in [bool_list, result_stack, operator_stack]:
                print l

        result_stack = []
        operator_stack = []

        def apply(op):
            function = self.OPS[op][0]
            arity = self.OPS[op][1]
            args = []
            for i in range(arity):
                args.append(result_stack.pop())
            return function(*args)

        for el in bool_list:

            if el in self.OPS:
                if operator_stack == [] or operator_stack[-1] == "(" or el == "NOT":
                    operator_stack.append(el)
                else:
                    operator = operator_stack.pop()
                    result_stack.append(apply(operator))
            elif el in self.parentheses:
                if el == "(":
                    operator_stack.append(el)
                else:
                    assert el == ")", el
                    try:
                        while operator_stack[-1] != "(":
                            operator = operator_stack.pop()
                            result_stack.append(apply(operator))
                        operator_stack.pop()
                    except IndexError, e:
                        raise TaggerException("Unbalanced parantheses.")
            else:
                result_stack.append(self.tag_ls(el))

        while operator_stack != []:
            operator = operator_stack.pop()
            result_stack.append(apply(operator))

        return result_stack.pop()

class TaggerException(Exception):
    pass

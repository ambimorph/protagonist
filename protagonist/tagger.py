import sys

class Tagger():

    def create_tagsystem(config, out=sys.stdout, err=sys.stderr):
        base_directory = config['base_directory']
        # This should always be called with an absolute Unicode base_directory.

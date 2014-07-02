#!/usr/bin/env python
# -*- coding: utf-8-with-signature-unix; fill-column: 77 -*-
# -*- indent-tabs-mode: nil -*-

# protagonist -- A tagsystem. Organises your files with non-hierarchical tags.
#
# This file is part of protagonist; see README.rst for licensing terms.

import os, re, sys

from setuptools import find_packages, setup

trove_classifiers=[
    u"Development Status :: 3 - Alpha",
    u"License :: OSI Approved :: GNU General Public License (GPL)",
    u"License :: DFSG approved",
    u"Intended Audience :: Developers",
    u"Operating System :: Unix",
    u"Natural Language :: English",
    u"Programming Language :: Python",
    u"Programming Language :: Python :: 2",
    u"Programming Language :: Python :: 2.7",
    u"Topic :: Software Development :: Libraries",
    ]

PKG=u'protagonist'
VERSIONFILE = os.path.join(PKG, u"_version.py")

import versioneer
versioneer.versionfile_source = VERSIONFILE
versioneer.versionfile_build = VERSIONFILE
versioneer.tag_prefix = PKG+u'-' # tags are like protagonist-1.2.0
versioneer.parentdir_prefix = PKG+u'-' # dirname like 'myproject-1.2.0'

doc_fnames=[ u'COPYING.rst', u'README.rst' ]

# In case we are building for a .deb with stdeb's sdist_dsc command, we put the
# docs in "share/doc/python-$PKG".
doc_loc = u"share/doc/" + PKG

data_files = []
"""
    (doc_loc, doc_fnames),
    (os.path.join(u'pyutil', u'data'), [os.path.join(u'pyutil', u'data', u'wordlist.txt')])
    ]

install_requires=[u'zbase32 >= 1.0']
"""

readmetext_bytes = open(u'README.rst').read()
readmetext_unicode = readmetext_bytes.decode('utf-8')
while readmetext_unicode[0] == u'\ufeff':
    readmetext_unicode = readmetext_unicode[1:]

setup(name=PKG,
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      description=u'A tagsystem. Organises your files with non-hierarchical tags.',
      long_description=readmetext_unicode,
      author=u"L. Amber Wilcox-O'Hearn",
      author_email=u'amber@cs.toronto.edu',
      url=u'https://github.com/ambimorph/protagonist' + PKG,
      license=u'GNU GPL', 
      packages=find_packages(),
      include_package_data=True,
      data_files=data_files,
      extras_require={u'pyblake2': [u'pyblake2 >= 0.9.3',]},
      #install_requires=install_requires,
      classifiers=trove_classifiers,
      entry_points = {
          u'console_scripts': [
              u'protag = protagonist.protag:main',
              ] },
      test_suite=PKG+u".test",
      zip_safe=False, # I prefer unzipped for easier access.
      )

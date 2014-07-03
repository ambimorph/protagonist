.. slideconf::
   :autoslides: True
   :theme: single-level

.. role:: red
.. role:: blue

=============================================
 Protagonist: Links, and Boolean Expressions
=============================================


Thursday, June 3rd, 2014

Overview
========

* The role of links
* A demo
* Parsing Boolean expressions

Structure
=========

Recall the structure of the tagsystem:

.. code::

  .
  ├── goodbye.txt
  ├── happy_birthday.txt
  ├── hello.txt
  ├── hi.txt
  └── .protagonist
      ├── tags
      │   ├── enter
      │   │   ├── 07b26f762733aefe9456cabd0ec4bd85be19ff3f.txt
      │   │   └── d2f799bb9610968a2efa8f7682d5f2f1d45163d7.txt
      │   └── exit
      │       └── 875e88d3892f23ec5e90c6d13718edfb3310447e.txt
      └── truenames
          ├── 07b26f762733aefe9456cabd0ec4bd85be19ff3f.txt
          ├── 875e88d3892f23ec5e90c6d13718edfb3310447e.txt
          └── d2f799bb9610968a2efa8f7682d5f2f1d45163d7.txt


Links
=====

* Hard links are conceptually easy.

  * Hard linked files **are the same file**.

* Symlinks are a bit different.

  * In unix, "Everything is a file".
  * A symlink is a file, whose contents are the text of the link.
  * Also, \*nix *labels* this file as being a symbolic link.

Links
=====

.. code::

   $ ln hi.txt hard.txt
   $ ln -s hi.txt soft.txt
   $ stat hi.txt | head -n 3

   File: `hi.txt'
   Size: 3               Blocks: 8          IO Block: 4096   regular file
   Device: 802h/2050d      Inode: 2299470     Links: 2

   $ stat hard.txt | head -n 3

   File: `hard.txt'
   Size: 3               Blocks: 8          IO Block: 4096   regular file
   Device: 802h/2050d      Inode: 2299470     Links: 2

   $ stat soft.txt | head -n 3

   File: `soft.txt' -> `hi.txt'
   Size: 6               Blocks: 0          IO Block: 4096   symbolic link
   Device: 802h/2050d      Inode: 2301113     Links: 1

Links
=====
   
* Almost all system calls automatically follow symbolic links:

.. code::

   $ cat hi.txt 
   hi

   $ cat soft.txt 
   hi

   $ readlink soft.txt 
   hi.txt


Protagonist tags
================

* *tags* are hard links.

  This allows direct access to the file contents through the tagsystem.

  Specifically, if I run `tahoe backup .protagonist`, it backs up the actual files linked into the subdirectories.

Protagonist truenames
=====================

* *truenames* are just like symbolic links, but I haven't told the filesystem.

  .. code::

     $ cat .protagonist/truenames/07b26f762733aefe9456cabd0ec4bd85be19ff3f.txt 

     /home/amber/play/hi.txt

  Running `tahoe backup .protagonist` will back up the contents of truenames files, which it would skip if it "knew" they were symlinks.


Parsing Boolean expressions
===========================

* Infix to Postfix Stack algorithm with 2 stacks:

  * result
  * op, for operators

  Read each token *t*.

  * *t* is an operand? Push to result.
  * *t* is an operator?

    * Top of op is empty or lower precedence?

      * Yes? Push *t*.
      * No? Pop the higher-precedence operator, *s*, push *s* to result, push *t* to op.

Infix to Postfix
================

A + B * C

+-------+------+-----------+
| token | ops  |result     |
+=======+======+===========+
| A     |      | A         |
+-------+------+-----------+
| \+    | \+   | A         |
+-------+------+-----------+
| B     | \+   | A B       |
+-------+------+-----------+
| \*    | \+ * |  A B      |
+-------+------+-----------+
| C     |      | A B C     |
+-------+------+-----------+
| <end >|      | A B C * + |
+-------+------+-----------+

   
Protagonist takes this algorithm, but passes the tokens to set operations before appending them to the result.

Tag1 OR Tag2



=============
 Protagonist
=============

Gist and constraints
====================

A *tagsystem*: organise files with non-hierarchical tags.

* Search with a Boolean query: `TAG-LS types AND NOT Haskell`

* Designed for compatibility with `Tahoe-LAFS` back up:

  * recursively backs up all files in a directory.
  * Does not natively represent symlinks, so it doesn't follow them.
  * Uses content-based hashing to prevent redudant storage.

Structure
=========

* Uses filesystem directory structures. 

  * For every tag t in the system there is a directory:

    * .protagonist/tags/t/

  * Any file that is tagged with t is given a unique identifier i based on the BLAKE2 hash of its contents, and then it is hard linked under that name into directory t.

    E.g. tag "hello.txt" with contents "foo", with the tag "bar" --->

    .protagonist/tags/bar/983ceba2afea8694cc933336b27b907f90c53a88.txt 

    which directly accesses the same file that "hello.txt" does.

Why Hard links
--------------

* If you move a file, the pointer in the tagsystem stays with the file.
* If you run `tahoe backup .protagonist`, it will copy the tagging directory organisation, and make a single copy of every file in the tagging system.

Why unique identifiers?
-----------------------

* If we simply tried to link "hello.txt" with its name, there could be a name collision.
* If we wanted to use the full path, we would have to emulate our original directory structure under the tag/t/ directory.


Why content-based hashing?
--------------------------

* Potential to discover duplicates.

  * If I have downloaded my favourite paper twice, the second time I try to tag it, I can be informed.

* Could allow integrity checking.

Why BLAKE2?
-----------

It's harder, better, stronger, faster than MD5.


Problem: not human readable
---------------------------

We add an index .protagonist/truenames/ that has a file corresponding to each tagged file in the system.

* Its name is the ID.
* Its contents is the string of the pathname.

(Note that this becomes broken if the original is moved.  I haven't thought about how to fix that yet.)




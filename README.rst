=============
 Protagonist
=============

Protagonist implements a *tagsystem*: it is used for tagging files non-hierarchically, so that they can be found with boolean queries.
Protagonist interfaces a particular filesystem structure (described below) that represents a tagsystem through the use of special directories and links.

(For usage examples, see EXAMPLES.rst.)

A major design constraint of this project is to provide seamless compatibility with Tahoe-LAFS_ backup storage.
Tahoe-LAFS backup will take a directory and recursively back up the files in every subdirectory.
It does not have a native representation of symbolic links.


Structure
=========

The tagsystem structure is defined in a special directory named ".protagonist/".

There is a subdirectory named ".protagonist/tags", and a subdirectory ".protagonist/tags/t" for every existing tag, t.
Any file which is tagged with t is given a unique identifier and a hard link in the directory t.

More generally, an intended future feature is that the tagsystem supports key-value pairs, with the directories ".protagonist/key/value/"

Why hard links?
---------------

Protagonist could be implemented with symbolic links, but hard links were chosen for the following reasons:

* For compatibility with Tahoe-LAFS_  backup storage.
* To enable reference counting and tracking logic.
* To reduce layers of indirection.

.. _Tahoe-LAFS: http://www.tahoe-lafs.org

Unique identifiers
------------------

For unique file identification, Protagonist uses the (20 byte) BLAKE2 hash of the contents at the time of tagging, with the same file extension as the original file.
The potential advantages of content-based hashing are:

* Recovery from file movement.
* Discovery of untagged files (could also be done with inodes).
* Identification of multiple copies of the same file.
* Enabling integrity checking of immutable files.

Using content-based hashing on mutable files will not have these advantages, though it could be used to help clarify intent, by, for example, allowing the user to specifically list files that should stay unchanged.

Using hard links has repercussions for deleting files that have been tagged.  With symlinks, a deleted or moved file will leave broken links.  With hard links, there needs to be special logic for determining whether the file exists outside of the tagsystem.
This is implemented in the command line interface, which wraps `rm` and `mv`.

Truenames
---------

A problem with using unique IDs is that now the result of a *tagls* is not recognisable to the user.
This motivates the truenames index.

Part of the goals of this project is to use the directory structure of the underlying filesystem as a primitive that can be used as a data structure.
Therefore, I wish to avoid symlinks and databases in favour of filesystem mechanisms.

The design I have chosen is to make a special directory called "truenames", where there is a file named with the file ID, the contents of which are the true pathname.
This is eerily like implementing symlinks.
It essentially *is* symlinks, but stealth symlinks, that aren't flagged as such in the inode tables, and therefore aren't followed by commands that normally follow symlinks.


Methods
=======

The tagsystem supports:

* addition and deletion of tags
* tagging and untagging files
* querying with boolean combinations
* cleanly removing and moving files from the filesystem even if they have been tagged.

creation of a tagsystem
-----------------------

The tagsystem is automatically created with the first tagging of a file.
Tagsystem creation is idempotent.  If there is already a tagsystem there, nothing is changed.

untagging files
---------------

When we wish to remove a tag, t, from a file, f:

* If f was the only file with tag t, then tag t should also be removed from the tagsystem.
* Because files with identical content have the same file id, a request to untag f, when f is not tagged, but an identical file f' is tagged could result in untagging the wrong file copy.  Therefore care must be taken to assure that f is the correct link in the file.  For this we will use inodes instead of content hashing.

deleting tags
-------------

Tag deletion can be done even if some files have the tag.  Those links just go away, and if I file is left with no tags, it is removed from the truenames index.

Dependencies
============

* `pyblake2 <https://github.com/dchest/pyblake2>`_


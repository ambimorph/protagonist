=============
 Protagonist
=============

Protagonist implements a *tagsystem*: it is used for tagging files non-hierarchically, so that they can be found with boolean queries.
Protagonist interfaces a particular filesystem structure (described below) that represents a tagsystem through the use of special directories and links.

*The remainder of this document is an on-going design specification that I am designing as I go, in tandem with the implementation.*

Structure
=========

The tagsystem structure is defined in a special directory named ".protagonist/".

There is a subdirectory named ".protagonist/tags", and a subdirectory ".protagonist/tags/t" for every existing tag, t.
Any file which is tagged with t is given a unique identifier and a hard link in the directory t.

More generally, the tagsystem supports key-value pairs, with the directories ".protagonist/key/value/"

Why hard links?
---------------

Protagonist could be implemented with symbolic links, but hard links were chosen for the following reasons:

* For compatibility with `Tahoe-LAFS <www.tahoe-lafs.org>`_ backup storage.
* To enable reference counting and tracking logic.
* To reduce layers of indirection.

Unique identifiers
------------------

For unique file identification, Protagonist will use the BLAKE2 hash of the contents at the time of tagging, with the same file extension as the original file.
The potential advantages of content-based hashing are:

* Recovery from file movement.
* Discovery of untagged files (could also be done with inodes).
* Identification of multiple copies of the same file.
* Enabling integrity checking of immutable files.

Using content-based hashing on mutable files will not have these advantages, though it could be used to help clarify intent, by, for example, allowing the user to specifically list files that should stay unchanged.

Using hard links will have repercussions for deleting files that have been tagged.  With symlinks, a deleted or moved file will leave broken links.  With hard links, there would need to be special logic for determining whether the file exists outside of the tagsystem.


Methods
=======

The tagsystem should support:

* creation of a new tagsystem
* addition and deletion of tags
* tagging and untagging files
* querying with boolean combinations

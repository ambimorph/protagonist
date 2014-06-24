USING: tools.test sequences kernel protagonist accessors io.files io.pathnames io.directories namespaces io.directories.hierarchy io.encodings.utf8 io.files.info ;
IN: protagonist.tests

! Let's go somewhere else to make messes.
"/tmp" absolute-path set-current-directory

! First create a tagsystem by making a base directory for tags to live in.
! Check that the directory is there.
[ t ] [ current-directory get tag-path exists? ] unit-test

! Make sure it is idempotent.
[ t ] [ current-directory get tag-path exists? ] unit-test

! Now let's reuse the same tagsystem for awhile.
SYMBOL: a-tag-path
current-directory get tag-path a-tag-path set

! Test that there isn't a tag.
[ t ] [ a-tag-path get directory-entries { } = ] unit-test

! Test that there isn't a specific tag.
[ f ] [ a-tag-path get "some-tag" tag-exists? ] unit-test

! Add a tag.
[ t ] [ a-tag-path get "some-tag" 2dup add-tag tag-exists? ] unit-test

! Here's a file and a tag.
SYMBOL: hello-file-path
"hellofile.txt" absolute-path hello-file-path set
"hello, world!\n" hello-file-path get utf8 set-file-contents

! Test file ids with md5.
[ t ] [ hello-file-path get make-file-id "910c8bc73110b0cd1bc5d2bcae782511.txt" = ]
unit-test


! Tag a file with a new tag.
[ t ]
[
  hello-file-path get dup make-file-id
  swap a-tag-path get "whee" tag-file
  a-tag-path get "whee" append-path prepend-path
  file-info ino>>
  hello-file-path get file-info ino>>
  =
] unit-test

! Let's clean up the mess.
a-tag-path get delete-tree

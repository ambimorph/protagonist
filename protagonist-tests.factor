USING: tools.test sequences kernel protagonist accessors io.files io.pathnames io.directories namespaces io.directories.hierarchy io.encodings.utf8 ;
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
"hellofile" absolute-path hello-file-path set
"hello, world!\n" hello-file-path get utf8 set-file-contents

! Tag a file with a new tag.
! (This tests that the file exists, but not that it is properly linked.)
[ t ]
[
  hello-file-path get dup make-file-id
  swap a-tag-path get "whee" tag-file
  a-tag-path get "whee" append-path prepend-path exists?
] unit-test

! Let's clean up the mess.
a-tag-path get delete-tree

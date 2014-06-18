USING: tools.test sequences kernel protagonist accessors io.files io.pathnames io.directories namespaces io.directories.hierarchy ;
IN: protagonist.tests

! Let's go somewhere else to make messes.
"/tmp" absolute-path set-current-directory

! First create a tagsystem by making a base directory for tags to live in.
! Check that the directory is there.
[ t ] [ <tagsystem> tag-path exists? ] unit-test

! Make sure it is idempotent.
[ t ] [ <tagsystem> tag-path exists? ] unit-test

! Now let's reuse the same tagsystem for awhile.
SYMBOL: a-tagsystem
<tagsystem> a-tagsystem set
SYMBOL: a-tag-path
a-tagsystem get tag-path a-tag-path set

! Test that there isn't a tag.
[ t ] [ a-tag-path get directory-entries { } = ] unit-test

! Test that there isn't a specific tag.
[ f ] [ "some-tag" a-tagsystem get tag-exists? ] unit-test

! Add a tag.
[ t ] [ "some-tag" a-tagsystem get 2dup add-tag tag-exists? ] unit-test

! Let's clean up the mess.
a-tag-path get delete-tree

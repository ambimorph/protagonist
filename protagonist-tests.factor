USING: tools.test sequences kernel protagonist accessors io.files io.pathnames io.directories namespaces ;
IN: protagonist.tests

! Let's go somewhere else to make messes.
"/tmp" absolute-path set-current-directory

! First create a tagsystem by making a base directory for tags to live in.
! Check that the directory is there.

[ t ]
[ <tagsystem> tag-path exists? ]
unit-test

! Make sure it is idempotent.

[ t ]
[ <tagsystem> tag-path exists? ]
unit-test

! Now let's reuse the same tagsystem for awhile.
SYMBOL: a-tag-path
<tagsystem> tag-path a-tag-path set

! Test that there isn't a tag.
[ t ]
[ a-tag-path get directory-entries { } = ]
unit-test

! Let's clean up the mess.
<tagsystem> tag-path delete-directory 

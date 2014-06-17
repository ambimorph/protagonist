USING: tools.test sequences kernel protagonist accessors io.files io.pathnames ;
IN: protagonist.tests

! First create a tagsystem by making a base directory for tags to live in.
! Check that the directory is there.

[ t ]
[ <tagsystem> tag-path exists? ]
unit-test

! Make sure it is idempotent.

[ t ]
[ <tagsystem> tag-path exists? ]
unit-test


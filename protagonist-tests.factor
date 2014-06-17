USING: tools.test sequences kernel protagonist accessors io.files io.pathnames ;
IN: protagonist.tests

! First create a tagsystem by making a base directory for tags to live in.
! Check that the directory is there.

[ t ]
[ tagsystem new dup create-tagsystem base-directory>> absolute-path ".protagonist" append-path exists? ]
unit-test

! Make sure it is idempotent.

[ t ]
[ tagsystem new dup create-tagsystem base-directory>> absolute-path ".protagonist" append-path exists? ]
unit-test


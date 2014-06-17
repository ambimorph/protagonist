USING: tools.test sequences kernel protagonist accessors io.files io.pathnames io.directories ;
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

! Let's clean up the mess.
<tagsystem> tag-path delete-directory 

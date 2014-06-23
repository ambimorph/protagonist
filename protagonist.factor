USING: io sequences kernel strings io.directories io.pathnames accessors io.files io.files.links ;
IN: protagonist

! TUPLE: tagsystem { base-directory string initial: "./" }
!                  { tag-directory string initial: ".protagonist" } ;

! : tag-path ( tagsystem -- string )
!     [ base-directory>>  absolute-path ] [ tag-directory>> ] bi append-path ;

: tag-path ( path -- path )
    ".protagonist" append-path dup exists?
    [ ] [ dup make-directory ] if ;

: tag-exists? ( string path -- ? )
    append-path exists? ;

: add-tag ( path string -- )
    2dup tag-exists?
    [ drop drop ] [ append-path make-directory ] if ;

: make-file-id ( path -- string )
    drop "2" ;

: tag-file ( path path string -- )
    ! file tag-path tag
    2dup add-tag append-path [ dup make-file-id ] dip swap append-path make-hard-link ;

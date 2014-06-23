USING: io sequences kernel strings io.directories io.pathnames accessors io.files io.files.links checksums checksums.md5 byte-arrays io.encodings.utf8 ;
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

! This is going to use md5 until I figure out how to get blake2 integrated.
: make-file-id ( path -- string )
    dup file-extension
    [ utf8 file-contents >byte-array md5 checksum-bytes hex-string ] dip
    [ "." append ] dip append ;

: tag-file ( path path string -- )
    ! file tag-path tag
    2dup add-tag append-path [ dup make-file-id ] dip prepend-path make-hard-link ;

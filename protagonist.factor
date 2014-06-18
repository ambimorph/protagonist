USING: io sequences kernel strings io.directories io.pathnames accessors io.files ;
IN: protagonist

TUPLE: tagsystem { base-directory string initial: "./" }
                 { tag-directory string initial: ".protagonist" } ;

: tag-path ( tagsystem -- string )
    [ base-directory>>  absolute-path ] [ tag-directory>> ] bi append-path ;

: <tagsystem> ( -- t ) tagsystem new
    dup tag-path dup exists?
    [ drop ] [ make-directory ] if ;

: tag-exists? ( string tagsystem -- ? )
    tag-path swap append-path exists? ;

: add-tag ( string tagsystem -- )
    2dup tag-exists?
    [ drop drop ] [ tag-path swap append-path make-directory ] if ;

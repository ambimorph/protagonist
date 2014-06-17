USING: io sequences kernel strings io.directories io.pathnames accessors io.files ;
IN: protagonist

TUPLE: tagsystem { base-directory string initial: "./" } ;
: create-tagsystem ( string -- )
    base-directory>> absolute-path ".protagonist" append-path dup exists?
    [ drop ] [ make-directory ] if ;


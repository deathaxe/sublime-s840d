; SYNTAX TEST "s840d_arc.sublime-syntax"

; ==================================================
;  CALL tests
;  Performance: 0.2ms
; ==================================================

; ---------------------------------------------------------------------
; valid FILE tag
%_N_CYCLE_SPF
; <- annotation.archive punctuation.definition.tag
;^^^^^^^^^^^^ annotation.archive entity.name.tag.dest-file
; ---------------------------------------------------------------------
; invalid FILE tag
%_N_CYCLE()_SPF
; <- annotation.archive punctuation.definition.tag
;^^^^^^^^^^^^^^ annotation.archive entity.name.tag.dest-file
;        ^^ invalid.illegal
; ---------------------------------------------------------------------
; valid PATH tag
%_N_CYCLE_SPF
;$PATH=/_N_CMA_DIR
; <- annotation.archive meta.mapping.key punctuation.definition.tag
;^^^^^^^^^^^^^^^^^ annotation.archive
;^^^^^ meta.mapping.key
;     ^ meta.mapping - meta.mapping.key - meta.mapping.value
;      ^^^^^^^^^^^ meta.mapping.value
;^ punctuation.definition.tag
; ^^^^ entity.other.attribute-name
;     ^ punctuation.separator.mapping.key-value
;      ^^^^^^^^^^^ entity.name.tag.dest-path.s840d_arc
; ---------------------------------------------------------------------
; PATH tag must not contain whitespace
%_N_CYCLE_SPF
;$PATH= /_N_CMA_DIR
; <- annotation.archive meta.mapping.key punctuation.definition.tag
;^^^^^^^^^^^^^^^^^^ annotation.archive
;^^^^^ meta.mapping.key
;     ^ meta.mapping - meta.mapping.key - meta.mapping.value
;      ^^^^^^^^^^^^ meta.mapping.value
; ^^^^ entity.other.attribute-name
;^ punctuation.definition.tag
;     ^ punctuation.separator.mapping.key-value
;      ^^^^^^^^^^^^ invalid.illegal.dest-path
%_N_CYCLE_SPF
;$PATH = /_N_CMA_DIR
; <- annotation.archive meta.mapping.key punctuation.definition.tag
;^^^^^^^^^^^^^^^^^^^ annotation.archive
;^^^^^ meta.mapping.key - meta.mapping.value
;      ^^^^^^^^^^^^^ meta.mapping - meta.mapping.key - meta.mapping.value
;^ punctuation.definition.tag
; ^^^^ entity.other.attribute-name
;      ^ - punctuation.separator.mapping.key-value
;     ^^^^^^^^^^^^^^ invalid.illegal.dest-path
; ---------------------------------------------------------------------
; PATH tag must not be preceded by a whitespace
%_N_CYCLE_SPF
; $PATH = /_N_CMA_DIR
; <- comment.line
;^^^^^^^^^^^^^^^^^^^^ comment.line - meta.mapping
; ---------------------------------------------------------------------
; PATH tag must not be indented
%_N_CYCLE_SPF
 ;$PATH = /_N_CMA_DIR
;^^^^^^^^^^^^^^^^^^^^ comment.line - meta.mapping
; ---------------------------------------------------------------------
; PATH tag must be upper case
%_N_CYCLE_SPF
;$PATH=/_n_cma_dir
; <- annotation.archive meta.mapping.key punctuation.definition.tag
;^^^^^^^^^^^^^^^^^ annotation.archive
;^^^^^ meta.mapping.key
;     ^ meta.mapping - meta.mapping.key - meta.mapping.value
;      ^^^^^^^^^^^ meta.mapping.value
; ^^^^ entity.other.attribute-name
;^ punctuation.definition.tag
;     ^ punctuation.separator.mapping.key-value
;      ^^^^^^^^^^^ invalid.illegal.dest-path
; PATH tag must be upper case
%_N_CYCLE_SPF
;$Path=/_n_cMa_Dir
; <- annotation.archive meta.mapping.key punctuation.definition.tag
;^^^^^^^^^^^^^^^^^ annotation.archive
;^^^^^^^^^^^^^^^^^ meta.mapping.key - meta.mapping.value
;^ punctuation.definition.tag
; ^^^^^^^^^^^^^^^^ invalid.illegal.dest-path
;     ^ - punctuation.separator.mapping.key-value

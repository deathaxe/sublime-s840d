; SYNTAX TEST "s840d_arc.sublime-syntax"

; ==================================================
;  CALL tests
;  Performance: 1.7ms
; ==================================================

; ---------------------------------------------------------------------
; valid FILE tag
%_N_CYCLE_SPF
; <- meta.annotation.archive punctuation.definition.tag
;^^^^^^^^^^^^ meta.annotation.archive entity.name.tag.dest-file
; ---------------------------------------------------------------------
; invalid FILE tag
%_N_CYCLE()_SPF
; <- meta.annotation.archive punctuation.definition.tag
;^^^^^^^^^^^^^^ meta.annotation.archive entity.name.tag.dest-file
;        ^^ invalid.illegal
; ---------------------------------------------------------------------
; valid PATH tag
%_N_CYCLE_SPF
;$PATH=/_N_CMA_DIR
; <- meta.annotation.archive meta.mapping.key punctuation.definition.tag
;^^^^^^^^^^^^^^^^^ meta.annotation.archive
;^^^^^ meta.mapping.key
;     ^ meta.mapping - meta.mapping.key - meta.mapping.value
;      ^^^^^^^^^^^ meta.mapping.value
;^ punctuation.definition.tag
; ^^^^ entity.other.attribute-name
;     ^ punctuation.separator.mapping.key-value
;      ^^^^^^^^^^^ entity.name.tag.dest-path.s840d_arc
; ---------------------------------------------------------------------
; valid PATH tag
%_N_CYCLE_SPF
;$PATH=/_N_CMA_DIR
;VERSION: 1.0.0.0 ;DATE: 2018-09-10
;         ^^^^^^^ constant.language.version
;          ^ punctuation.separator.sequence
;            ^ punctuation.separator.sequence
;              ^ punctuation.separator.sequence
;                        ^^^^^^^^^^ constant.language.date
;                            ^ punctuation.separator.sequence
;                               ^ punctuation.separator.sequence
; ---------------------------------------------------------------------
; PATH tag must not contain whitespace
%_N_CYCLE_SPF
;$PATH= /_N_CMA_DIR
; <- meta.annotation.archive meta.mapping.key punctuation.definition.tag
;^^^^^^^^^^^^^^^^^^ meta.annotation.archive
;^^^^^ meta.mapping.key
;     ^ meta.mapping - meta.mapping.key - meta.mapping.value
;      ^^^^^^^^^^^^ meta.mapping.value
; ^^^^ entity.other.attribute-name
;^ punctuation.definition.tag
;     ^ punctuation.separator.mapping.key-value
;      ^^^^^^^^^^^^ invalid.illegal.dest-path
%_N_CYCLE_SPF
;$PATH = /_N_CMA_DIR
; <- meta.annotation.archive meta.mapping.key punctuation.definition.tag
;^^^^^^^^^^^^^^^^^^^ meta.annotation.archive
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
; <- meta.annotation.archive meta.mapping.key punctuation.definition.tag
;^^^^^^^^^^^^^^^^^ meta.annotation.archive
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
; <- meta.annotation.archive meta.mapping.key punctuation.definition.tag
;^^^^^^^^^^^^^^^^^ meta.annotation.archive meta.mapping.key - meta.mapping.value
;^ punctuation.definition.tag
; ^^^^^^^^^^^^^^^^ invalid.illegal.dest-path
;     ^ - punctuation.separator.mapping.key-value

; check correct bailouts
%_N_MY_TEXT_COM
;$PATH=/_N_COM_DIR
85000 0 0 "my text"
;<- source.s840d_arc source.s840d_hmi meta.stringlist - source.s840d_hmi source.s840d_hmi - meta.annotation
;^^^^^^^^^^^^^^^^^^ source.s840d_hmi meta.stringlist - source.s840d_hmi source.s840d_hmi
%_N_MY_MASK_COM
;$PATH=/_N_COM_DIR
//G(my_mask//10/0,0)
; <- source.s840d_arc source.s840d_hmi meta.class.grid - source.s840d_hmi source.s840d_hmi - meta.annotation
;^^^^^^^^^^^^^^^^^^^ source.s840d_arc source.s840d_hmi meta.class.grid - source.s840d_hmi source.s840d_hmi
//END    ; //G(my_mask)
; <- source.s840d_hmi meta.class.grid
;^^^^ source.s840d_hmi meta.class.grid
%_N_INITIAL_INI
N11660 $MN_NUM_EG=10
; <- source.s840d_arc source.s840d_gcode comment.blockno.s840d_gcode - source.s840d_gcode.tea source.s840d_gcode.tea - meta.annotation
;^^^^^^^^^^^^^^^^^^^ source.s840d_arc source.s840d_gcode.tea - source.s840d_gcode.tea source.s840d_gcode.tea
;^^^^^ comment.blockno.s840d_gcode
;      ^ punctuation.definition.variable.nck.s840d_gcode
;       ^^^^^^^^^ support.variable.nck.machdata.s840d_gcode
;                ^ keyword.operator.assignment.s840d_gcode
;                 ^^ constant.numeric.integer.s840d_gcode
%_N_CYCLE_SPF
;$PATH=/_N_CMA_DIR
PROC MYCYC(INT _VAR) ACTBLOCNO
;<- source.s840d_arc source.s840d_gcode.spf meta.function - source.s840d_gcode.tea source.s840d_gcode.tea - meta.annotation
;^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ source.s840d_arc source.s840d_gcode.spf meta.function - source.s840d_gcode.spf source.s840d_gcode.spf
;^^^ keyword.declaration.proc.s840d_gcode
;    ^^^^^ entity.name.function.s840d_gcode
;         ^ punctuation.section.parameters.begin.s840d_gcode
;          ^^^ storage.type.s840d_gcode
;              ^^^^ variable.parameter.procedure.s840d_gcode
;                  ^ punctuation.section.parameters.end.s840d_gcode
;                    ^^^^^^^^^ storage.modifier.function.s840d_gcode
%_N_MAIN_MPF
;$PATH=/_N_WKS_DIR/_N_FOO_DIR
N10 MYCYC(0)
;<- source.s840d_arc source.s840d_gcode.mpf comment.blockno.s840d_gcode - source.s840d_gcode.mpf source.s840d_gcode.mpf - meta.annotation
;^^^^^^^^^^^ source.s840d_arc source.s840d_gcode.mpf - source.s840d_gcode.mpf source.s840d_gcode.mpf
%_N_INVALID_TXT
;$PATH=/_N_WKS_DIR/_N_FOO_DIR
This is plain text
;<- source.s840d_arc text.plain
;^^^^^^^^^^^^^^^^^^ source.s840d_arc text.plain

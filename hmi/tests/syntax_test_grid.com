; SYNTAX TEST "s840d_hmi.sublime-syntax"

; ==================================================
;  //G tests
;  Performance: 0.3ms
; ==================================================

; Grid definition
//G(GRID_NAME/0/10/1/1)
;                      <- meta.class.grid
;   ^^^^^^^^^ meta.class.grid.parameters.name
;             ^ meta.class.grid.parameters.type
;               ^^ meta.class.grid.parameters.row.count
;                  ^ meta.class.grid.parameters.row.fixed
;                    ^ meta.class.grid.parameters.col.fixed
;  ^ punctuation.section.parameters.begin
;   ^^^^^^^^^ entity.name.class
;            ^ punctuation.separator
;             ^ constant.numeric.integer
;              ^ punctuation.separator
;               ^^ constant.numeric.integer
;                 ^ punctuation.separator
;                  ^ constant.numeric.integer
;                   ^ punctuation.separator
;                    ^ constant.numeric.integer
;                     ^ punctuation.section.parameters.end
; Column definition
(IDD/1,10/0/"tooltip","caption"/WR0/"PIC.PNG"/"DB10.DBB100"/100/10)
;<- punctuation.section.column.begin
;                                                                 <- meta.column
;^^^ meta.column.type
;    ^^^^ meta.column.limits
;         ^ meta.column.default
;           ^^^^^^^^^^^^^^^^^^^ meta.column.captions
;                               ^^^ meta.column.attributes
;                                   ^^^^^^^^^ meta.column.picture
;                                             ^^^^^^^^^^^^^ meta.column.address
;                                                           ^^^ meta.column.width
;                                                               ^^ meta.column.offsets
;^^^ storage.type
;   ^ punctuation.separator
;    ^ constant.numeric.integer
;     ^ punctuation.separator
;      ^^ constant.numeric.integer
;        ^ punctuation.separator
;         ^ constant.numeric.integer
;          ^ punctuation.separator
;           ^ punctuation.definition.string.begin
;           ^^^^^^^^^ string.quoted.double
;                   ^ punctuation.definition.string.end
;                    ^ punctuation.separator
;                     ^ punctuation.definition.string.begin
;                     ^^^^^^^^^ string.quoted.double
;                             ^ punctuation.definition.string.end
;                              ^ punctuation.separator
;                               ^^^ constant.language.attribute
;                                  ^ punctuation.separator
;                                   ^ punctuation.definition.string.begin
;                                   ^^^^^^^^^ string.quoted.double
;                                           ^ punctuation.definition.string.end
;                                            ^ punctuation.separator
;                                             ^ punctuation.definition.string.begin
;                                             ^^^^^^^^^^^^^ string.quoted.double
;                                                         ^ punctuation.definition.string.end
;                                                          ^ punctuation.separator
;                                                           ^^^ constant.numeric.integer
;                                                              ^ punctuation.separator
;                                                               ^^ constant.numeric.integer
;                                                                 ^ punctuation.section.column.end
//END
;    <- meta.class.grid.end
;    <- keyword.declaration.class.end

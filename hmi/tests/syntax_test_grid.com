; SYNTAX TEST "s840d_hmi.sublime-syntax"

; ==================================================
;  //G tests
;  Performance: 0.4ms
; ==================================================


//G
; <- meta.class.grid.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;^^ meta.class.grid.s840d_hmi keyword.declaration.class.begin.s840d_hmi
//G
; <- meta.class.grid.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;^^ meta.class.grid.s840d_hmi keyword.declaration.class.begin.s840d_hmi
//END
;<- meta.class.grid.s840d_hmi keyword.declaration.class.end.s840d_hmi
;^^^^ meta.class.grid.s840d_hmi keyword.declaration.class.end.s840d_hmi

//G()
;^^^^^ - meta.class.grid meta.class.grid
; <- meta.class.grid.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;^^ meta.class.grid.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;  ^ meta.class.grid.parameters.name.s840d_hmi meta.parens.s840d_hmi punctuation.section.parens.begin.s840d_hmi
;   ^ meta.class.grid.parameters.name.s840d_hmi meta.parens.s840d_hmi punctuation.section.parens.end.s840d_hmi
//END
;^^^^ - meta.class.grid meta.class.grid
;<- meta.class.grid.s840d_hmi keyword.declaration.class.end.s840d_hmi
;^^^^ meta.class.grid.s840d_hmi keyword.declaration.class.end.s840d_hmi

//G(
;^^^^ - meta.class.grid meta.class.grid
; <- meta.class.grid.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;^^ meta.class.grid.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;  ^ meta.class.grid.parameters.name.s840d_hmi meta.parens.s840d_hmi punctuation.section.parens.begin.s840d_hmi
//END
;^^^^ - meta.class.grid meta.class.grid
;<- meta.class.grid.s840d_hmi keyword.declaration.class.end.s840d_hmi
;^^^^ meta.class.grid.s840d_hmi keyword.declaration.class.end.s840d_hmi

//G(name)
;^^^^^^^^^ - meta.class.grid meta.class.grid
; <- meta.class.grid.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;^^ meta.class.grid.s840d_hmi
;  ^^^^^^ meta.class.grid.parameters.name.s840d_hmi meta.parens.s840d_hmi
;        ^ meta.class.grid.s840d_hmi
;^^ keyword.declaration.class.begin.s840d_hmi
;  ^ punctuation.section.parens.begin.s840d_hmi
;   ^^^^ entity.name.class.s840d_hmi
;       ^ punctuation.section.parens.end.s840d_hmi
//END
;^^^^ - meta.class.grid meta.class.grid
;<- meta.class.grid.s840d_hmi keyword.declaration.class.end.s840d_hmi
;^^^^ meta.class.grid.s840d_hmi keyword.declaration.class.end.s840d_hmi

//G illegal
;^^^^^^^^^^^ - meta.class.grid meta.class.grid
; <- meta.class.grid.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;^^^^^^^^^^^ meta.class.grid.s840d_hmi
;^^ keyword.declaration.class.begin.s840d_hmi
;   ^^^^^^^ invalid.illegal.s840d_hmi
//END
;^^^^ - meta.class.grid meta.class.grid
;<- meta.class.grid.s840d_hmi keyword.declaration.class.end.s840d_hmi
;^^^^ meta.class.grid.s840d_hmi keyword.declaration.class.end.s840d_hmi

//G(name illegal) illegal ; comment
;^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ - meta.class.grid meta.class.grid
; <- meta.class.grid.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;^^ meta.class.grid.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;  ^^^^^^^^^^^^^^ meta.class.grid.parameters.name.s840d_hmi meta.parens.s840d_hmi
;                ^^^^^^^^^^^^^^^^^^^ meta.class.grid.s840d_hmi
;  ^ punctuation.section.parens.begin.s840d_hmi
;   ^^^^ entity.name.class.s840d_hmi
;        ^^^^^^^ invalid.illegal.s840d_hmi
;               ^ punctuation.section.parens.end.s840d_hmi
;                 ^^^^^^^ invalid.illegal.s840d_hmi
;                         ^^^^^^^^^^ comment.line.s840d_hmi
//END
;^^^^ - meta.class.grid meta.class.grid
;<- meta.class.grid.s840d_hmi keyword.declaration.class.end.s840d_hmi
;^^^^ meta.class.grid.s840d_hmi keyword.declaration.class.end.s840d_hmi

//G(GRID_NAME/0/10/1,1)
;<- meta.class.grid.s840d_hmi
;^^ meta.class.grid.s840d_hmi
;  ^^^^^^^^^^^ meta.class.grid.parameters.name.s840d_hmi
;             ^^ meta.class.grid.parameters.type.s840d_hmi
;               ^^^ meta.class.grid.parameters.row.count.s840d_hmi
;                  ^^ meta.class.grid.parameters.row.fixed.s840d_hmi
;                    ^^ meta.class.grid.parameters.col.fixed.s840d_hmi
;  ^ punctuation.section.parens.begin
;   ^^^^^^^^^ entity.name.class
;            ^ punctuation.separator
;             ^ constant.numeric.integer
;              ^ punctuation.separator
;               ^^ constant.numeric.integer
;                 ^ punctuation.separator
;                  ^ constant.numeric.integer
;                   ^ punctuation.separator
;                    ^ constant.numeric.integer
;                     ^ punctuation.section.parens.end
; Column definition
(IDD/1,10/0/"tooltip","caption"/WR0/"PIC.PNG"/"DB10.DBB100"/100/10)
;^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ - meta.column meta.column
;<- meta.class.grid.body.s840d_hmi meta.block.s840d_hmi meta.column.type.s840d_hmi meta.parens.s840d_hmi
;^^^ meta.class.grid.body.s840d_hmi meta.block.s840d_hmi meta.column.type.s840d_hmi meta.parens.s840d_hmi
;    ^^^^ meta.class.grid.body.s840d_hmi meta.block.s840d_hmi meta.column.limits.s840d_hmi meta.parens.s840d_hmi
;         ^ meta.class.grid.body.s840d_hmi meta.block.s840d_hmi meta.column.default.s840d_hmi meta.parens.s840d_hmi
;           ^^^^^^^^^^^^^^^^^^^ meta.class.grid.body.s840d_hmi meta.block.s840d_hmi meta.column.captions.s840d_hmi meta.parens.s840d_hmi
;                               ^^^ meta.class.grid.body.s840d_hmi meta.block.s840d_hmi meta.column.attributes.s840d_hmi meta.parens.s840d_hmi
;                                   ^^^^^^^^^ meta.class.grid.body.s840d_hmi meta.block.s840d_hmi meta.column.picture.s840d_hmi meta.parens.s840d_hmi
;                                             ^^^^^^^^^^^^^ meta.class.grid.body.s840d_hmi meta.block.s840d_hmi meta.column.address.s840d_hmi meta.parens.s840d_hmi
;                                                           ^^^ meta.class.grid.body.s840d_hmi meta.block.s840d_hmi meta.column.width.s840d_hmi meta.parens.s840d_hmi
;                                                               ^^ meta.class.grid.body.s840d_hmi meta.block.s840d_hmi meta.column.offsets.s840d_hmi meta.parens.s840d_hmi
;<- punctuation.section.parens.begin.s840d_hmi
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
;                                                                 ^ punctuation.section.parens.end
//END
;<- meta.class.grid.s840d_hmi keyword.declaration.class.end.s840d_hmi
;^^^^ meta.class.grid.s840d_hmi keyword.declaration.class.end.s840d_hmi

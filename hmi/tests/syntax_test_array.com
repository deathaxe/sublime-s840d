; SYNTAX TEST "s840d_hmi.sublime-syntax"

; ==================================================
;  //A tests
;  Performance: 0.3ms
; ==================================================

//A
; <- meta.class.array.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;^^ meta.class.array.s840d_hmi keyword.declaration.class.begin.s840d_hmi
//A
; <- meta.class.array.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;^^ meta.class.array.s840d_hmi keyword.declaration.class.begin.s840d_hmi
//END
;<- meta.class.array.s840d_hmi keyword.declaration.class.end.s840d_hmi
;^^^^ meta.class.array.s840d_hmi keyword.declaration.class.end.s840d_hmi

//A()
;^^^^^ - meta.class.array meta.class.array
; <- meta.class.array.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;^^ meta.class.array.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;  ^ meta.class.array.parameters.name.s840d_hmi meta.parens.s840d_hmi punctuation.section.parens.begin.s840d_hmi
;   ^ meta.class.array.parameters.name.s840d_hmi meta.parens.s840d_hmi punctuation.section.parens.end.s840d_hmi
//END
;^^^^ - meta.class.array meta.class.array
;<- meta.class.array.s840d_hmi keyword.declaration.class.end.s840d_hmi
;^^^^ meta.class.array.s840d_hmi keyword.declaration.class.end.s840d_hmi

//A(
;^^^^ - meta.class.array meta.class.array
; <- meta.class.array.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;^^ meta.class.array.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;  ^ meta.class.array.parameters.name.s840d_hmi meta.parens.s840d_hmi punctuation.section.parens.begin.s840d_hmi
//END
;^^^^ - meta.class.array meta.class.array
;<- meta.class.array.s840d_hmi keyword.declaration.class.end.s840d_hmi
;^^^^ meta.class.array.s840d_hmi keyword.declaration.class.end.s840d_hmi

//A(name)
;^^^^^^^^^ - meta.class.array meta.class.array
; <- meta.class.array.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;^^ meta.class.array.s840d_hmi
;  ^^^^^^ meta.class.array.parameters.name.s840d_hmi meta.parens.s840d_hmi
;        ^ meta.class.array.s840d_hmi
;^^ keyword.declaration.class.begin.s840d_hmi
;  ^ punctuation.section.parens.begin.s840d_hmi
;   ^^^^ entity.name.class.s840d_hmi
;       ^ punctuation.section.parens.end.s840d_hmi
//END
;^^^^ - meta.class.array meta.class.array
;<- meta.class.array.s840d_hmi keyword.declaration.class.end.s840d_hmi
;^^^^ meta.class.array.s840d_hmi keyword.declaration.class.end.s840d_hmi

//A illegal
;^^^^^^^^^^^ - meta.class.array meta.class.array
; <- meta.class.array.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;^^^^^^^^^^^ meta.class.array.s840d_hmi
;^^ keyword.declaration.class.begin.s840d_hmi
;   ^^^^^^^ invalid.illegal.s840d_hmi
//END
;^^^^ - meta.class.array meta.class.array
;<- meta.class.array.s840d_hmi keyword.declaration.class.end.s840d_hmi
;^^^^ meta.class.array.s840d_hmi keyword.declaration.class.end.s840d_hmi

//A(name illegal) illegal ; comment
;^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ - meta.class.array meta.class.array
; <- meta.class.array.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;^^ meta.class.array.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;  ^^^^^^^^^^^^^^ meta.class.array.parameters.name.s840d_hmi meta.parens.s840d_hmi
;                ^^^^^^^^^^^^^^^^^^^ meta.class.array.s840d_hmi
;  ^ punctuation.section.parens.begin.s840d_hmi
;   ^^^^ entity.name.class.s840d_hmi
;        ^^^^^^^ invalid.illegal.s840d_hmi
;               ^ punctuation.section.parens.end.s840d_hmi
;                 ^^^^^^^ invalid.illegal.s840d_hmi
;                         ^^^^^^^^^^ comment.line.s840d_hmi
//END
;^^^^ - meta.class.array meta.class.array
;<- meta.class.array.s840d_hmi keyword.declaration.class.end.s840d_hmi
;^^^^ meta.class.array.s840d_hmi keyword.declaration.class.end.s840d_hmi

//A(name)
    (
;   ^ meta.class.array.body.s840d_hmi meta.block.s840d_hmi meta.row.s840d_hmi meta.parens.s840d_hmi punctuation.section.parens.begin.s840d_hmi
    )
;   ^ meta.class.array.body.s840d_hmi meta.block.s840d_hmi invalid.illegal.s840d_hmi
    (/
;   ^^ meta.class.array.body.s840d_hmi meta.block.s840d_hmi meta.row.s840d_hmi meta.parens.s840d_hmi
;   ^ punctuation.section.parens.begin.s840d_hmi
;    ^ punctuation.separator.column.s840d_hmi
    ( )
;   ^^^ meta.class.array.body.s840d_hmi meta.block.s840d_hmi meta.row.s840d_hmi meta.parens.s840d_hmi
;   ^ punctuation.section.parens.begin.s840d_hmi
;     ^ punctuation.section.parens.end.s840d_hmi
    (/)
;   ^^^ meta.class.array.body.s840d_hmi meta.block.s840d_hmi meta.row.s840d_hmi meta.parens.s840d_hmi
;   ^ punctuation.section.parens.begin.s840d_hmi
;    ^ punctuation.separator.column.s840d_hmi
;     ^ punctuation.section.parens.end.s840d_hmi
    (10/true/"string")
;   ^^^^^^^^^^^^^^^^^^ meta.class.array.body.s840d_hmi meta.block.s840d_hmi meta.row.s840d_hmi meta.parens.s840d_hmi
;   ^ punctuation.section.parens.begin.s840d_hmi
;    ^^ constant.numeric.integer.s840d_hmi
;      ^ punctuation.separator.column.s840d_hmi
;       ^^^^ constant.language.boolean.s840d_hmi
;           ^ punctuation.separator.column.s840d_hmi
;            ^^^^^^^^ string.quoted.double.s840d_hmi
;                    ^ punctuation.section.parens.end.s840d_hmi
//END
;^^^^ - meta.class.array meta.class.array
;<- meta.class.array.s840d_hmi keyword.declaration.class.end.s840d_hmi
;^^^^ meta.class.array.s840d_hmi keyword.declaration.class.end.s840d_hmi

; SYNTAX TEST "s840d_hmi.sublime-syntax"

; ==================================================
;  //B tests
;  Performance: 0.5ms
; ==================================================

//B
; <- meta.class.subprogram.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;^^ meta.class.subprogram.s840d_hmi keyword.declaration.class.begin.s840d_hmi
//B
; <- meta.class.subprogram.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;^^ meta.class.subprogram.s840d_hmi keyword.declaration.class.begin.s840d_hmi
//END
;<- meta.class.subprogram.s840d_hmi keyword.declaration.class.end.s840d_hmi
;^^^^ meta.class.subprogram.s840d_hmi keyword.declaration.class.end.s840d_hmi

//B()
;^^^^^ - meta.class.subprogram meta.class.subprogram
; <- meta.class.subprogram.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;^^ meta.class.subprogram.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;  ^ meta.class.subprogram.parameters.name.s840d_hmi meta.parens.s840d_hmi punctuation.section.parens.begin.s840d_hmi
;   ^ meta.class.subprogram.parameters.name.s840d_hmi meta.parens.s840d_hmi punctuation.section.parens.end.s840d_hmi
//END
;^^^^ - meta.class.subprogram meta.class.subprogram
;<- meta.class.subprogram.s840d_hmi keyword.declaration.class.end.s840d_hmi
;^^^^ meta.class.subprogram.s840d_hmi keyword.declaration.class.end.s840d_hmi

//B(
;^^^^ - meta.class.subprogram meta.class.subprogram
; <- meta.class.subprogram.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;^^ meta.class.subprogram.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;  ^ meta.class.subprogram.parameters.name.s840d_hmi meta.parens.s840d_hmi punctuation.section.parens.begin.s840d_hmi
//END
;^^^^ - meta.class.subprogram meta.class.subprogram
;<- meta.class.subprogram.s840d_hmi keyword.declaration.class.end.s840d_hmi
;^^^^ meta.class.subprogram.s840d_hmi keyword.declaration.class.end.s840d_hmi

//B(name)
;^^^^^^^^^ - meta.class.subprogram meta.class.subprogram
; <- meta.class.subprogram.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;^^ meta.class.subprogram.s840d_hmi
;  ^^^^^^ meta.class.subprogram.parameters.name.s840d_hmi meta.parens.s840d_hmi
;        ^ meta.class.subprogram.s840d_hmi
;^^ keyword.declaration.class.begin.s840d_hmi
;  ^ punctuation.section.parens.begin.s840d_hmi
;   ^^^^ entity.name.class.s840d_hmi
;       ^ punctuation.section.parens.end.s840d_hmi
//END
;^^^^ - meta.class.subprogram meta.class.subprogram
;<- meta.class.subprogram.s840d_hmi keyword.declaration.class.end.s840d_hmi
;^^^^ meta.class.subprogram.s840d_hmi keyword.declaration.class.end.s840d_hmi

//B illegal
;^^^^^^^^^^^ - meta.class.subprogram meta.class.subprogram
; <- meta.class.subprogram.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;^^^^^^^^^^^ meta.class.subprogram.s840d_hmi
;^^ keyword.declaration.class.begin.s840d_hmi
;   ^^^^^^^ invalid.illegal.s840d_hmi
//END
;^^^^ - meta.class.subprogram meta.class.subprogram
;<- meta.class.subprogram.s840d_hmi keyword.declaration.class.end.s840d_hmi
;^^^^ meta.class.subprogram.s840d_hmi keyword.declaration.class.end.s840d_hmi

//B(name illegal) illegal ; comment
;^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ - meta.class.subprogram meta.class.subprogram
; <- meta.class.subprogram.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;^^ meta.class.subprogram.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;  ^^^^^^^^^^^^^^ meta.class.subprogram.parameters.name.s840d_hmi meta.parens.s840d_hmi
;                ^^^^^^^^^^^^^^^^^^^ meta.class.subprogram.s840d_hmi
;  ^ punctuation.section.parens.begin.s840d_hmi
;   ^^^^ entity.name.class.s840d_hmi
;        ^^^^^^^ invalid.illegal.s840d_hmi
;               ^ punctuation.section.parens.end.s840d_hmi
;                 ^^^^^^^ invalid.illegal.s840d_hmi
;                         ^^^^^^^^^^ comment.line.s840d_hmi
//END
;^^^^ - meta.class.subprogram meta.class.subprogram
;<- meta.class.subprogram.s840d_hmi keyword.declaration.class.end.s840d_hmi
;^^^^ meta.class.subprogram.s840d_hmi keyword.declaration.class.end.s840d_hmi

//B(name)

//END
;^^^^ - meta.class.subprogram meta.class.subprogram
;<- meta.class.subprogram.s840d_hmi keyword.declaration.class.end.s840d_hmi
;^^^^ meta.class.subprogram.s840d_hmi keyword.declaration.class.end.s840d_hmi

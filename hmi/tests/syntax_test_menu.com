; SYNTAX TEST "s840d_hmi.sublime-syntax"

; ==================================================
;  //S tests
;  Performance: 0.3ms
; ==================================================

//S
; <- meta.class.menu.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;^^ meta.class.menu.s840d_hmi keyword.declaration.class.begin.s840d_hmi
//S
; <- meta.class.menu.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;^^ meta.class.menu.s840d_hmi keyword.declaration.class.begin.s840d_hmi
//END
;<- meta.class.menu.s840d_hmi keyword.declaration.class.end.s840d_hmi
;^^^^ meta.class.menu.s840d_hmi keyword.declaration.class.end.s840d_hmi

//S()
;^^^^^ - meta.class.menu meta.class.menu
; <- meta.class.menu.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;^^ meta.class.menu.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;  ^ meta.class.menu.parameters.name.s840d_hmi meta.parens.s840d_hmi punctuation.section.parens.begin.s840d_hmi
;   ^ meta.class.menu.parameters.name.s840d_hmi meta.parens.s840d_hmi punctuation.section.parens.end.s840d_hmi
//END
;^^^^ - meta.class.menu meta.class.menu
;<- meta.class.menu.s840d_hmi keyword.declaration.class.end.s840d_hmi
;^^^^ meta.class.menu.s840d_hmi keyword.declaration.class.end.s840d_hmi

//S(
;^^^^ - meta.class.menu meta.class.menu
; <- meta.class.menu.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;^^ meta.class.menu.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;  ^ meta.class.menu.parameters.name.s840d_hmi meta.parens.s840d_hmi punctuation.section.parens.begin.s840d_hmi
//END
;^^^^ - meta.class.menu meta.class.menu
;<- meta.class.menu.s840d_hmi keyword.declaration.class.end.s840d_hmi
;^^^^ meta.class.menu.s840d_hmi keyword.declaration.class.end.s840d_hmi

//S( ; comment
;^^^^ - meta.class.menu meta.class.menu
; <- meta.class.menu.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;^^ meta.class.menu.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;  ^^^^^^^^^^^^ meta.class.menu.parameters.name.s840d_hmi meta.parens.s840d_hmi
;  ^ punctuation.section.parens.begin.s840d_hmi
;    ^^^^^^^^^^ comment.line.s840d_hmi
//END
;^^^^ - meta.class.menu meta.class.menu
;<- meta.class.menu.s840d_hmi keyword.declaration.class.end.s840d_hmi
;^^^^ meta.class.menu.s840d_hmi keyword.declaration.class.end.s840d_hmi

//S(name)
;^^^^^^^^^ - meta.class.menu meta.class.menu
; <- meta.class.menu.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;^^ meta.class.menu.s840d_hmi
;  ^^^^^^ meta.class.menu.parameters.name.s840d_hmi meta.parens.s840d_hmi
;        ^ meta.class.menu.s840d_hmi
;^^ keyword.declaration.class.begin.s840d_hmi
;  ^ punctuation.section.parens.begin.s840d_hmi
;   ^^^^ entity.name.class.s840d_hmi
;       ^ punctuation.section.parens.end.s840d_hmi
//END
;^^^^ - meta.class.menu meta.class.menu
;<- meta.class.menu.s840d_hmi keyword.declaration.class.end.s840d_hmi
;^^^^ meta.class.menu.s840d_hmi keyword.declaration.class.end.s840d_hmi

//S illegal
;^^^^^^^^^^^ - meta.class.menu meta.class.menu
; <- meta.class.menu.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;^^^^^^^^^^^ meta.class.menu.s840d_hmi
;^^ keyword.declaration.class.begin.s840d_hmi
;   ^^^^^^^ invalid.illegal.s840d_hmi
//END
;^^^^ - meta.class.menu meta.class.menu
;<- meta.class.menu.s840d_hmi keyword.declaration.class.end.s840d_hmi
;^^^^ meta.class.menu.s840d_hmi keyword.declaration.class.end.s840d_hmi

//S(name illegal) illegal ; comment
;^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ - meta.class.menu meta.class.menu
; <- meta.class.menu.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;^^ meta.class.menu.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;  ^^^^^^^^^^^^^^ meta.class.menu.parameters.name.s840d_hmi meta.parens.s840d_hmi
;                ^^^^^^^^^^^^^^^^^^^ meta.class.menu.s840d_hmi
;  ^ punctuation.section.parens.begin.s840d_hmi
;   ^^^^ entity.name.class.s840d_hmi
;        ^^^^^^^ invalid.illegal.s840d_hmi
;               ^ punctuation.section.parens.end.s840d_hmi
;                 ^^^^^^^ invalid.illegal.s840d_hmi
;                         ^^^^^^^^^^ comment.line.s840d_hmi
//END
;^^^^ - meta.class.menu meta.class.menu
;<- meta.class.menu.s840d_hmi keyword.declaration.class.end.s840d_hmi
;^^^^ meta.class.menu.s840d_hmi keyword.declaration.class.end.s840d_hmi

//S(MNU_NAME, "translate1.txt", "translate2.txt"/)
;^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ - meta.class.menu meta.class.menu
;^^ meta.class.menu.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;  ^^^^^^^^^^ meta.class.menu.parameters.name.s840d_hmi meta.parens.s840d_hmi
;            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ meta.class.menu.parameters.langfiles.s840d_hmi
;                                                ^ meta.class.menu.parameters.s840d_hmi
;                                                 ^ meta.class.menu.s840d_hmi
;   ^^^^^^^^ entity.name.class.s840d_hmi
;           ^ punctuation.separator.parameters.s840d_hmi
;             ^^^^^^^^^^^^^^^^ string.quoted.double.s840d_hmi
;                             ^ punctuation.separator.s840d_hmi
;                               ^^^^^^^^^^^^^^^^ string.quoted.double.s840d_hmi
;                                               ^ invalid.illegal.separator.s840d_hmi
;                                                ^ punctuation.section.parens.end.s840d_hmi
//END
;^^^^ - meta.class.menu meta.class.menu
;<- meta.class.menu.s840d_hmi keyword.declaration.class.end.s840d_hmi
;^^^^ meta.class.menu.s840d_hmi keyword.declaration.class.end.s840d_hmi

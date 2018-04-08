; SYNTAX TEST "s840d_hmi.sublime-syntax"

; ==================================================
;  //M tests
;  Performance: 0.9ms
; ==================================================

//M(NAME/"TITLE"/"PIC"/0,0,640,480/"VAR"/20,20,64,64/PA1/129/"LANG.COM")
;<- meta.class.dialog
;^^ meta.class.dialog - meta.class.dialog.parameters
;  ^ meta.class.dialog.parameters
;   ^^^^^ meta.class.dialog.parameters.name
;        ^^^^^^^^ meta.class.dialog.parameters.caption
;                ^^^^^^ meta.class.dialog.parameters.picture
;                      ^^^^^^^^^^^^ meta.class.dialog.parameters.dimension
;                                  ^^^^^^ meta.class.dialog.parameters.variable
;                                        ^^^^^^^^^^^^ meta.class.dialog.parameters.picture-position
;                                                    ^^^^ meta.class.dialog.parameters.attributes
;                                                        ^^^^ meta.class.dialog.parameters.background
;                                                            ^^^^^^^^^^^ meta.class.dialog.parameters.langfiles
;                                                                       ^ meta.class.dialog.body
;<- keyword.class.begin
;^^ keyword.class.begin
;  ^ punctuation.section.parameters.begin
;   ^^^^ entity.name.class
;       ^ punctuation.separator
;        ^ punctuation.definition.string.begin
;        ^^^^^^^ string.quoted.double
;              ^ punctuation.definition.string.end
;               ^ punctuation.separator
;                ^ punctuation.definition.string.begin
;                ^^^^^ string.quoted.double
;                    ^ punctuation.definition.string.end
;                     ^ punctuation.separator
;                      ^ constant.numeric.integer
;                       ^ punctuation.separator
;                        ^ constant.numeric.integer
;                         ^ punctuation.separator
;                          ^^^ constant.numeric.integer
;                             ^ punctuation.separator
;                              ^^^ constant.numeric.integer
;                                 ^ punctuation.separator
;                                  ^ punctuation.definition.string.begin
;                                  ^^^^^ string.quoted.double
;                                      ^ punctuation.definition.string.end
;                                       ^ punctuation.separator
;                                        ^^ constant.numeric.integer
;                                          ^ punctuation.separator
;                                           ^^ constant.numeric.integer
;                                             ^ punctuation.separator
;                                              ^^ constant.numeric.integer
;                                                ^ punctuation.separator
;                                                 ^^ constant.numeric.integer
;                                                   ^ punctuation.separator
;                                                    ^^^ constant.language.attribute
;                                                       ^ punctuation.separator
;                                                        ^^^ constant.numeric.integer
;                                                           ^ punctuation.separator
;                                                            ^ punctuation.definition.string.begin
;                                                            ^^^^^^^^^^ string.quoted.double
;                                                                     ^ punctuation.definition.string.end
DEF FOO, BAR, BAZ ; comment
;<- meta.class.dialog.body
;^^^^^^^^^^^^^^^^^^^^^^^^^^^ meta.class.dialog.body
;<- meta.operand
;^^^^^^^^^^^^^^^^^^^^^^^^^^^ meta.operand
;   ^^^ variable.other
;      ^ punctuation.separator
;        ^^^ variable.other
;           ^ punctuation.separator
;             ^^^ variable.other
;                 ^^^^^^^^^^ comment.line
DEF FOO, BAR,
;<- meta.class.dialog.body
;^^^^^^^^^^^^ meta.class.dialog.body
;<- meta.operand
;^^^^^^^^^^^^ meta.operand
;   ^^^ variable.other
;      ^ punctuation.separator
;        ^^^ variable.other
;           ^ punctuation.separator
    BAZ ; comment
;<- meta.class.dialog.body
;^^^^^^^^^^^^^^^^ meta.class.dialog.body
;<- meta.operand
;^^^^^^^^^^^^^^^^ meta.operand
;   ^^^ variable.other
;       ^^^^^^^^^ comment.line
DEF FOO, BAR, ; comment
;<- meta.class.dialog.body
;^^^^^^^^^^^^^^^^^^^^^^ meta.class.dialog.body
;<- meta.operand
;^^^^^^^^^^^^^^^^^^^^^^ meta.operand
;   ^^^ variable.other
;      ^ punctuation.separator
;        ^^^ variable.other
;           ^ punctuation.separator
;             ^^^^^^^^^^ comment.line
    BAZ ; comment
;<- meta.class.dialog.body
;^^^^^^^^^^^^^^^^ meta.class.dialog.body
;<- meta.operand
;^^^^^^^^^^^^^^^^ meta.operand
;   ^^^ variable.other
;       ^^^^^^^^^ comment.line
DEF FOO(2), BAR(44), BAZ(5) ; comment
;<- meta.class.dialog.body
;^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ meta.class.dialog.body
;<- meta.operand
;^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ meta.operand
;   ^^^ variable.other
;      ^ punctuation.section.array-size.begin
;       ^ constant.numeric.integer
;        ^ punctuation.section.array-size.end
;         ^ punctuation.separator
;           ^^^ variable.other
;              ^ punctuation.section.array-size.begin
;               ^^ constant.numeric.integer
;                 ^ punctuation.section.array-size.end
;                  ^ punctuation.separator
;                    ^^^ variable.other
;                       ^ punctuation.section.array-size.begin
;                        ^ constant.numeric.integer
;                         ^ punctuation.section.array-size.end
;                           ^^^^^^^^^ comment.line
DEF FOO(2), BAR(44), ; comment
;<- meta.class.dialog.body
;^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ meta.class.dialog.body
;<- meta.operand
;^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ meta.operand
;   ^^^ variable.other
;      ^ punctuation.section.array-size.begin
;       ^ constant.numeric.integer
;        ^ punctuation.section.array-size.end
;         ^ punctuation.separator
;           ^^^ variable.other
;              ^ punctuation.section.array-size.begin
;               ^^ constant.numeric.integer
;                 ^ punctuation.section.array-size.end
;                  ^ punctuation.separator
;                    ^^^^^^^^^ comment.line
    BAZ(5) ; comment
;<- meta.class.dialog.body
;^^^^^^^^^^^^^^^^^^^ meta.class.dialog.body
;<- meta.operand
;^^^^^^^^^^^^^^^^^^^ meta.operand
;   ^^^ variable.other
;      ^ punctuation.section.array-size.begin
;       ^ constant.numeric.integer
;        ^ punctuation.section.array-size.end
;          ^^^^^^^^^ comment.line
DEF FOO = (I/0,100) ; comment
;<- meta.class.dialog.body
;^^^^^^^^^^^^^^^^^^^^^^^^^^^^ meta.class.dialog.body
;<- meta.operand
;^^^^^^^^^ meta.operand - meta.operand.parameters
;         ^ meta.operand.parameters - meta.operand.parameters.type
;          ^^ meta.operand.parameters.type
;            ^^^^^^ meta.operand.parameters.limits
;          ^ storage.type
;           ^ punctuation.separator
;            ^ constant.numeric.integer
;             ^ punctuation.separator
;              ^^^ constant.numeric.integer
DEF FOO = (I/*0="off", 1 = "on" ) ; comment
;<- meta.class.dialog.body
;^^^^^^^^^^^^^^^^^^^^^^^^^^^^ meta.class.dialog.body
;<- meta.operand
;^^^^^^^^^ meta.operand - meta.operand.parameters
;         ^ meta.operand.parameters - meta.operand.parameters.type
;          ^^ meta.operand.parameters.type
;            ^^^^^^^^^^^^^^^^^^^^ meta.operand.parameters.list
;          ^ storage.type
;           ^ punctuation.separator
;            ^ punctuation.definition.keyword
;             ^ constant.numeric.integer
;              ^ keyword.operator.assignment
;               ^ punctuation.definition.string.begin
;               ^^^^^ string.quoted.double
;                   ^ punctuation.definition.string.end
;                    ^ punctuation.separator
;                      ^ constant.numeric.integer
;                        ^ keyword.operator.assignment
;                          ^ punctuation.definition.string.begin
;                          ^^^^ string.quoted.double
;                             ^ punctuation.definition.string.end
DEF FOO = (I/ %grid_name ) ; comment
;<- meta.class.dialog.body
;^^^^^^^^^^^^^^^^^^^^^^^^^^^^ meta.class.dialog.body
;<- meta.operand
;^^^^^^^^^ meta.operand - meta.operand.parameters
;         ^ meta.operand.parameters - meta.operand.parameters.type
;          ^^ meta.operand.parameters.type
;            ^^^^^^^^^^^^^ meta.operand.parameters.grid
;          ^ storage.type
;           ^ punctuation.separator
;             ^ punctuation.definition.keyword
;              ^^^^^^^^^ entity.name.grid
DEF FOO = (S32),
;   ^^^ variable.other
;              ^ punctuation.separator
    BAR = (I)
;   ^^^ variable.other
DEF FOO = (IDB),
;   ^^^ variable.other
;              ^ punctuation.separator
DEF BAR = (V)
;<- invalid.illegal.keyword
;^^ invalid.illegal.keyword
;   ^^^ variable.other
DEF FOO(2) = (S32), ; comment
;<- meta.class.dialog.body meta.operand
;^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ meta.class.dialog.body
;^^^^^^ meta.operand
;      ^^^ meta.operand.array-size
;         ^^^ meta.operand
;            ^^^^^ meta.operand.parameters
;<- keyword.language.def
;^^ keyword.language.def
;   ^^^ variable.other
;      ^ punctuation.section.array-size.begin
;       ^ constant.numeric.integer
;        ^ punctuation.section.array-size.end
    BAR(2) = (IDD///,"POS"/WR0///370,,90)
;   ^^^ variable.other
;      ^ punctuation.section.array-size.begin
;       ^ constant.numeric.integer
;        ^ punctuation.section.array-size.end

//END    ; //M(NAME)
; <- meta.class.dialog.end keyword.class.end
;^^^^ meta.class.dialog.end keyword.class.end
;    ^^^^^^^^^^^^^^^ - meta.class
;        ^^^^^^^^^^^ comment.line

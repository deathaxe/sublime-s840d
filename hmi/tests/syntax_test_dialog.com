; SYNTAX TEST "s840d_hmi.sublime-syntax"

; ==================================================
;  //M tests
;  Performance: 4.6ms
; ==================================================


//M
; <- meta.class.dialog.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;^^ meta.class.dialog.s840d_hmi keyword.declaration.class.begin.s840d_hmi
//M
; <- meta.class.dialog.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;^^ meta.class.dialog.s840d_hmi keyword.declaration.class.begin.s840d_hmi
//END
;<- meta.class.dialog.s840d_hmi keyword.declaration.class.end.s840d_hmi
;^^^^ meta.class.dialog.s840d_hmi keyword.declaration.class.end.s840d_hmi

//M()
;^^^^^ - meta.class.dialog meta.class.dialog
; <- meta.class.dialog.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;^^ meta.class.dialog.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;  ^ meta.class.dialog.parameters.name.s840d_hmi meta.parens.s840d_hmi punctuation.section.parens.begin.s840d_hmi
;   ^ meta.class.dialog.parameters.name.s840d_hmi meta.parens.s840d_hmi punctuation.section.parens.end.s840d_hmi
//END
;^^^^ - meta.class.dialog meta.class.dialog
;<- meta.class.dialog.s840d_hmi keyword.declaration.class.end.s840d_hmi
;^^^^ meta.class.dialog.s840d_hmi keyword.declaration.class.end.s840d_hmi

//M(
;^^^^ - meta.class.dialog meta.class.dialog
; <- meta.class.dialog.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;^^ meta.class.dialog.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;  ^ meta.class.dialog.parameters.name.s840d_hmi meta.parens.s840d_hmi punctuation.section.parens.begin.s840d_hmi
//END
;^^^^ - meta.class.dialog meta.class.dialog
;<- meta.class.dialog.s840d_hmi keyword.declaration.class.end.s840d_hmi
;^^^^ meta.class.dialog.s840d_hmi keyword.declaration.class.end.s840d_hmi

//M(name)
;^^^^^^^^^ - meta.class.dialog meta.class.dialog
; <- meta.class.dialog.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;^^ meta.class.dialog.s840d_hmi
;  ^^^^^^ meta.class.dialog.parameters.name.s840d_hmi meta.parens.s840d_hmi
;        ^ meta.class.dialog.s840d_hmi
;^^ keyword.declaration.class.begin.s840d_hmi
;  ^ punctuation.section.parens.begin.s840d_hmi
;   ^^^^ entity.name.class.s840d_hmi
;       ^ punctuation.section.parens.end.s840d_hmi
//END
;^^^^ - meta.class.dialog meta.class.dialog
;<- meta.class.dialog.s840d_hmi keyword.declaration.class.end.s840d_hmi
;^^^^ meta.class.dialog.s840d_hmi keyword.declaration.class.end.s840d_hmi

//M illegal
;^^^^^^^^^^^ - meta.class.dialog meta.class.dialog
; <- meta.class.dialog.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;^^^^^^^^^^^ meta.class.dialog.s840d_hmi
;^^ keyword.declaration.class.begin.s840d_hmi
;   ^^^^^^^ invalid.illegal.s840d_hmi
//END
;^^^^ - meta.class.dialog meta.class.dialog
;<- meta.class.dialog.s840d_hmi keyword.declaration.class.end.s840d_hmi
;^^^^ meta.class.dialog.s840d_hmi keyword.declaration.class.end.s840d_hmi

//M(name illegal) illegal ; comment
;^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ - meta.class.dialog meta.class.dialog
; <- meta.class.dialog.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;^^ meta.class.dialog.s840d_hmi keyword.declaration.class.begin.s840d_hmi
;  ^^^^^^^^^^^^^^ meta.class.dialog.parameters.name.s840d_hmi meta.parens.s840d_hmi
;                ^^^^^^^^^^^^^^^^^^^ meta.class.dialog.s840d_hmi
;  ^ punctuation.section.parens.begin.s840d_hmi
;   ^^^^ entity.name.class.s840d_hmi
;        ^^^^^^^ invalid.illegal.s840d_hmi
;               ^ punctuation.section.parens.end.s840d_hmi
;                 ^^^^^^^ invalid.illegal.s840d_hmi
;                         ^^^^^^^^^^ comment.line.s840d_hmi
//END
;^^^^ - meta.class.dialog meta.class.dialog
;<- meta.class.dialog.s840d_hmi keyword.declaration.class.end.s840d_hmi
;^^^^ meta.class.dialog.s840d_hmi keyword.declaration.class.end.s840d_hmi

//M
; <- meta.class.dialog.s840d_hmi keyword.declaration.class.begin.s840d_hmi
RESUME
; <- meta.class.dialog.body.s840d_hmi meta.block.s840d_hmi keyword.declaration.function
//M
; <- meta.class.dialog.s840d_hmi keyword.declaration.class.begin.s840d_hmi
RESOLUTION
; <- meta.class.dialog.body.s840d_hmi meta.block.s840d_hmi keyword.declaration.function
//M
; <- meta.class.dialog.s840d_hmi keyword.declaration.class.begin.s840d_hmi
SUB
; <- meta.class.dialog.body.s840d_hmi meta.block.s840d_hmi meta.method.sub.s840d_hmi keyword.declaration.method

//M(NAME/"TITLE"/"PIC"/0,0,640,480/"VAR"/20,20,64,64/PA1/129/"LANG.COM")
;^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ - meta.class.dialog meta.class.dialog
;<- meta.class.dialog.s840d_hmi
;^^ meta.class.dialog.s840d_hmi
;  ^^^^^^ meta.class.dialog.parameters.name.s840d_hmi
;        ^^^^^^^^ meta.class.dialog.parameters.caption.s840d_hmi
;                ^^^^^^ meta.class.dialog.parameters.picture.s840d_hmi
;                      ^^^^^^^^^^^^ meta.class.dialog.parameters.dimension.s840d_hmi
;                                  ^^^^^^ meta.class.dialog.parameters.variable.s840d_hmi
;                                        ^^^^^^^^^^^^ meta.class.dialog.parameters.picture-position.s840d_hmi
;                                                    ^^^^ meta.class.dialog.parameters.attributes.s840d_hmi
;                                                        ^^^^ meta.class.dialog.parameters.background.s840d_hmi
;                                                            ^^^^^^^^^^^ meta.class.dialog.parameters.langfiles.s840d_hmi
;                                                                       ^ meta.class.dialog.s840d_hmi
;<- keyword.declaration.class.begin.s840d_hmi
;^^ keyword.declaration.class.begin.s840d_hmi
;  ^ punctuation.section.parens.begin.s840d_hmi
;   ^^^^ entity.name.class.s840d_hmi
;       ^ punctuation.separator.s840d_hmi
;        ^ punctuation.definition.string.begin.s840d_hmi
;        ^^^^^^^ string.quoted.double.s840d_hmi
;              ^ punctuation.definition.string.end.s840d_hmi
;               ^ punctuation.separator.s840d_hmi
;                ^ punctuation.definition.string.begin.s840d_hmi
;                ^^^^^ string.quoted.double.s840d_hmi
;                    ^ punctuation.definition.string.end.s840d_hmi
;                     ^ punctuation.separator.s840d_hmi
;                      ^ constant.numeric.integer.s840d_hmi
;                       ^ punctuation.separator.s840d_hmi
;                        ^ constant.numeric.integer.s840d_hmi
;                         ^ punctuation.separator.s840d_hmi
;                          ^^^ constant.numeric.integer.s840d_hmi
;                             ^ punctuation.separator.s840d_hmi
;                              ^^^ constant.numeric.integer.s840d_hmi
;                                 ^ punctuation.separator.s840d_hmi
;                                  ^ punctuation.definition.string.begin.s840d_hmi
;                                  ^^^^^ string.quoted.double.s840d_hmi
;                                      ^ punctuation.definition.string.end.s840d_hmi
;                                       ^ punctuation.separator.s840d_hmi
;                                        ^^ constant.numeric.integer.s840d_hmi
;                                          ^ punctuation.separator.s840d_hmi
;                                           ^^ constant.numeric.integer.s840d_hmi
;                                             ^ punctuation.separator.s840d_hmi
;                                              ^^ constant.numeric.integer.s840d_hmi
;                                                ^ punctuation.separator.s840d_hmi
;                                                 ^^ constant.numeric.integer.s840d_hmi
;                                                   ^ punctuation.separator.s840d_hmi
;                                                    ^^^ constant.language.attribute.scaling.pictures.s840d_hmi
;                                                       ^ punctuation.separator.s840d_hmi
;                                                        ^^^ constant.numeric.integer.s840d_hmi
;                                                           ^ punctuation.separator.s840d_hmi
;                                                            ^ punctuation.definition.string.begin.s840d_hmi
;                                                            ^^^^^^^^^^ string.quoted.double.s840d_hmi
;                                                                     ^ punctuation.definition.string.end.s840d_hmi
;                                                                      ^ punctuation.section.parens.end.s840d_hmi
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
;            ^^^^^^^^^^^^^^^^^^^^ meta.operand.parameters.array
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
DEF FOO = (I/ *array_name ) ; comment
;<- meta.class.dialog.body
;^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ meta.class.dialog.body
;<- meta.operand
;^^^^^^^^^ meta.operand - meta.operand.parameters
;         ^ meta.operand.parameters - meta.operand.parameters.type
;          ^^ meta.operand.parameters.type
;            ^^^^^^^^^^^^^^ meta.operand.parameters.array
;          ^ storage.type
;           ^ punctuation.separator
;             ^ punctuation.definition.keyword
;              ^^^^^^^^^^ entity.name.array
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
;<- keyword.declaration.def
;^^ keyword.declaration.def
;   ^^^ variable.other
;      ^ punctuation.section.array-size.begin
;       ^ constant.numeric.integer
;        ^ punctuation.section.array-size.end
    BAR(2) = (IDD/0,999/10/"desc","short","unit"/WR0/"\\pic.png"/"$A_MINUTE"/10,10,90,16/100,10,50,16/10,20/"help.html"/"mm"/)
;            ^ meta.operand.parameters - meta.operand.parameters.type
;             ^^^^ meta.operand.parameters.type
;                 ^^^^^^ meta.operand.parameters.limits
;                       ^^^ meta.operand.parameters.default
;                          ^^^^^^^^^^^^^^^^^^^^^^ meta.operand.parameters.captions
;                                                ^^^^ meta.operand.parameters.attributes
;                                                    ^^^^^^^^^^^^ meta.operand.parameters.picture
;                                                                ^^^^^^^^^^^^ meta.operand.parameters.address
;                                                                            ^^^^^^^^^^^^ meta.operand.parameters.position.caption
;                                                                                        ^^^^^^^^^^^^^ meta.operand.parameters.position.input
;                                                                                                     ^^^^^^ meta.operand.parameters.colors
;                                                                                                           ^^^^^^^^^^^^ meta.operand.parameters.helpfile
;                                                                                                                       ^^^^^ meta.operand.parameters.units
;                                                                                                                            ^ meta.operand.parameters - meta.operand.parameters.type
;                                                                                                                             ^ - meta.operand
;   ^^^ variable.other
;      ^ punctuation.section.array-size.begin
;       ^ constant.numeric.integer
;        ^ punctuation.section.array-size.end
;          ^ keyword.operator.assignment
;            ^ punctuation.section.parameters.begin
;             ^^^ storage.type
;                ^ punctuation.separator
;                 ^ constant.numeric.integer
;                  ^ punctuation.separator
;                   ^^^ constant.numeric.integer
;                      ^ punctuation.separator
;                       ^^ constant.numeric.integer
;                         ^ punctuation.separator
;                          ^ punctuation.definition.string.begin
;                          ^^^^^^ string.quoted.double
;                               ^ punctuation.definition.string.end
;                                ^ punctuation.separator
;                                 ^ punctuation.definition.string.begin
;                                 ^^^^^^^ string.quoted.double
;                                       ^ punctuation.definition.string.end
;                                        ^ punctuation.separator
;                                         ^ punctuation.definition.string.begin
;                                         ^^^^^^ string.quoted.double
;                                              ^ punctuation.definition.string.end
;                                               ^ punctuation.separator
;                                                ^^^ constant.language.attribute
;                                                   ^ punctuation.separator
;                                                    ^ punctuation.definition.string.begin
;                                                    ^^^^^^^^^^^ string.quoted.double
;                                                              ^ punctuation.definition.string.end
;                                                               ^ punctuation.separator
;                                                                ^ string.quoted.double punctuation.definition.string.begin
;                                                                 ^^^^^^^^^ support.variable
;                                                                          ^ string.quoted.double punctuation.definition.string.end
;                                                                           ^ punctuation.separator
;                                                                            ^^ constant.numeric.integer
;                                                                              ^ punctuation.separator
;                                                                               ^^ constant.numeric.integer
;                                                                                 ^ punctuation.separator
;                                                                                  ^^ constant.numeric.integer
;                                                                                    ^ punctuation.separator
;                                                                                     ^^ constant.numeric.integer
;                                                                                       ^ punctuation.separator
;                                                                                        ^^^ constant.numeric.integer
;                                                                                           ^ punctuation.separator
;                                                                                            ^^ constant.numeric.integer
;                                                                                              ^ punctuation.separator
;                                                                                               ^^ constant.numeric.integer
;                                                                                                 ^ punctuation.separator
;                                                                                                  ^^ constant.numeric.integer
;                                                                                                    ^ punctuation.separator
;                                                                                                     ^^ constant.numeric.integer
;                                                                                                       ^ punctuation.separator
;                                                                                                        ^^ constant.numeric.integer
;                                                                                                          ^ punctuation.separator
;                                                                                                           ^ punctuation.definition.string.begin
;                                                                                                           ^^^^^^^^^^^ string.quoted.double
;                                                                                                                     ^ punctuation.definition.string.end
;                                                                                                                      ^ punctuation.separator
;                                                                                                                       ^ punctuation.definition.string.begin
;                                                                                                                       ^^^^ string.quoted.double
;                                                                                                                          ^ punctuation.definition.string.end
;                                                                                                                           ^ invalid.illegal.separator
;                                                                                                                            ^ punctuation.section.parameters.end

; SOFTKEY DEFINITION TESTS
  HS1 = ( "caption", AC4, SE2, TP0 ) ; horizontal softkey
; ^^^^^^ meta.softkey - meta.softkey.parameters.caption
;       ^ meta.softkey.parameters - meta.softkey.parameters.caption
;        ^^^^^^^^^^^ meta.softkey.parameters.caption - meta.softkey.parameters.attributes
;                   ^^^^^^^^^^^^^^^^ meta.softkey.parameters.attributes - meta.softkey.parameters.caption
;                                   ^ - meta.softkey
; ^^^ entity.name.softkey
;     ^ keyword.operator.assignment
;       ^ punctuation.section.parameters.begin
;         ^ punctuation.definition.string.begin
;         ^^^^^^^^^ string.quoted.double
;                 ^ punctuation.definition.string.end
;                  ^ punctuation.separator
;                    ^^^ constant.language.attribute.accesslevel
;                       ^ punctuation.separator
;                         ^^^ constant.language.attribute.state
;                            ^ punctuation.separator
;                              ^^^ constant.language.attribute.alignment.text
;                                  ^ punctuation.section.parameters.end
;                                    ^^^^^^^^^^^^^^^^^^^^^ comment.line
  VS1 = ( ["\\icon.png", "caption"], AC3, SE3, TP1 ) ; horizontal softkey
; ^^^^^^ meta.softkey - meta.softkey.parameters.caption
;       ^ meta.softkey.parameters - meta.softkey.parameters.caption
;        ^^^^^^^^^^^^^^^^^^^^^^^^^^^ meta.softkey.parameters.caption - meta.softkey.parameters.attributes
;                                   ^^^^^^^^^^^^^^^^ meta.softkey.parameters.attributes - meta.softkey.parameters.caption
;                                                   ^ - meta.softkey
;        ^ - meta.caption-group
;         ^^^^^^^^^^^^^^^^^^^^^^^^^ meta.caption-group
;                                  ^ - meta.caption-group
; ^^^ entity.name.softkey
;     ^ keyword.operator.assignment
;       ^ punctuation.section.parameters.begin
;         ^ punctuation.section.caption-group.begin
;          ^ punctuation.definition.string.begin
;          ^^^^^^^^^^^^ string.quoted.double
;                     ^ punctuation.definition.string.end
;                      ^ punctuation.separator
;                        ^ punctuation.definition.string.begin
;                        ^^^^^^^^^ string.quoted.double
;                                ^ punctuation.definition.string.end
;                                 ^ punctuation.section.caption-group.end
;                                  ^ punctuation.separator
;                                    ^^^ constant.language.attribute.accesslevel
;                                       ^ punctuation.separator
;                                         ^^^ constant.language.attribute.state
;                                            ^ punctuation.separator
;                                              ^^^ constant.language.attribute.alignment.text
;                                                  ^ punctuation.section.parameters.end
;                                                    ^^^^^^^^^^^^^^^^^^^^^ comment.line
  VS6 = ($86008)
; ^^^^^^ meta.softkey - meta.softkey.parameters.caption
;       ^ meta.softkey.parameters - meta.softkey.parameters.caption
;        ^^^^^^^ meta.softkey.parameters.caption - meta.softkey.parameters.attributes
;               ^ - meta.softkey
; ^^^ entity.name.softkey
;     ^ keyword.operator.assignment
;       ^ punctuation.section.parameters.begin
;        ^^^^^^ variable.language.textid
;              ^ punctuation.section.parameters.end
  VS7 = (["\\icon.png", $86008])
; ^^^^^^ meta.softkey - meta.softkey.parameters.caption
;       ^ meta.softkey.parameters - meta.softkey.parameters.caption
;        ^^^^^^^^^^^^^^^^^^^^^^^ meta.softkey.parameters.caption
;                               ^ - meta.softkey
; ^^^ entity.name.softkey
;     ^ keyword.operator.assignment
;       ^ punctuation.section.parameters.begin
;        ^ punctuation.section.caption-group.begin
;         ^ punctuation.definition.string.begin
;         ^^^^^^^^^^^^ string.quoted.double
;                    ^ punctuation.definition.string.end
;                     ^ punctuation.separator
;                       ^^^^^^ variable.language.textid
;                             ^ punctuation.section.caption-group.end
;                              ^ punctuation.section.parameters.end
  VS8 = (SOFTKEY_BACK, SE2)
; ^^^^^^ meta.softkey - meta.softkey.parameters.caption
;       ^ meta.softkey.parameters - meta.softkey.parameters.caption
;        ^^^^^^^^^^^^^ meta.softkey.parameters.caption - meta.softkey.parameters.attributes
;                     ^^^^^ meta.softkey.parameters.attributes - meta.softkey.parameters.caption
;                          ^ - meta.softkey
; ^^^ entity.name.softkey
;     ^ keyword.operator.assignment
;       ^ punctuation.section.parameters.begin
;        ^^^^^^^^^^^^ variable.language.softkeyid
;                    ^ punctuation.separator
;                      ^^^ constant.language.attribute.state
;                         ^ punctuation.section.parameters.end

CHANGE(var_name)
; <- meta.class.dialog.body keyword.declaration.function.change.begin
;^^^^^^^^^^^^^^^^ meta.class.dialog.body
;     ^^^^^^^^^^ meta.function.parameters.change
;^^^^^ keyword.declaration.function.change.begin
;     ^ punctuation.section.parameters.begin
;      ^^^^^^^^ variable.other
;              ^ punctuation.section.parameters.end
END_CHANGE
; <- meta.class.dialog.body keyword.declaration.function.change.end
;^^^^^^^^^ meta.class.dialog.body keyword.declaration.function.change.end

CHANNEL
; <- meta.class.dialog.body keyword.declaration.function.channel.begin
;^^^^^^ meta.class.dialog.body keyword.declaration.function.channel.begin
END_CHANNEL
; <- meta.class.dialog.body keyword.declaration.function.channel.end
;^^^^^^^^^^ meta.class.dialog.body keyword.declaration.function.channel.end

CONTROL
; <- meta.class.dialog.body keyword.declaration.function.control.begin
;^^^^^^ meta.class.dialog.body keyword.declaration.function.control.begin
END_CONTROL
; <- meta.class.dialog.body keyword.declaration.function.control.end
;^^^^^^^^^^ meta.class.dialog.body keyword.declaration.function.control.end

FOCUS(var_name)
; <- meta.class.dialog.body keyword.declaration.function.focus.begin
;^^^^^^^^^^^^^^^ meta.class.dialog.body
;    ^^^^^^^^^^ meta.function.parameters.focus
;^^^^ keyword.declaration.function.focus.begin
;    ^ punctuation.section.parameters.begin
;     ^^^^^^^^ variable.other
;             ^ punctuation.section.parameters.end
END_FOCUS
; <- meta.class.dialog.body keyword.declaration.function.focus.end
;^^^^^^^^ meta.class.dialog.body keyword.declaration.function.focus.end

LANGUAGE
; <- meta.class.dialog.body keyword.declaration.function.language.begin
;^^^^^^^ meta.class.dialog.body keyword.declaration.function.language.begin
    DLGL(S_LANG)
;<- meta.class.dialog.body meta.block.method.language
;^^^^^^^^^^^^^^^^ meta.class.dialog.body meta.block.method.language
;   ^^^^ meta.function-call.identifier.s840d_hmi
;       ^^^^^^^^ meta.function-call.arguments.s840d_hmi
;   ^^^^ support.function
;       ^ punctuation.section.parens.begin
;        ^^^^^^ support.variable.language
;              ^ punctuation.section.parens.end
END_LANGUAGE
; <- meta.class.dialog.body keyword.declaration.function.language.end
;^^^^^^^^^^^ meta.class.dialog.body keyword.declaration.function.language.end

; METHOD SYNTAX TESTS
LOAD
; <- meta.class.dialog.body keyword.declaration.function.load.begin
;^^^ meta.class.dialog.body keyword.declaration.function.load.begin
    Hd="dialog title"
; <- meta.class.dialog.body meta.block.method.load
;^^^^^^^^^^^^^^^^^^^^^ meta.class.dialog.body meta.block.method.load
;   ^^ entity.other.attribute-name
;     ^ keyword.operator.assignment
;      ^ punctuation.definition.string.begin
;      ^^^^^^^^^^^^^^ string.quoted.double
;                   ^ punctuation.definition.string.end
    VS1.ac=7
; <- meta.class.dialog.body meta.block.method.load
;^^^^^^^^^^^^ meta.class.dialog.body meta.block.method.load
;   ^^^ entity.name.softkey
;      ^ punctuation.accessor
;       ^^ entity.other.attribute-name
;         ^ keyword.operator.assignment
;          ^ constant.numeric.integer
    FOO.val = RNP( "DB10.DBB25" )
; <- meta.class.dialog.body meta.block.method.load
;^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ meta.class.dialog.body meta.block.method.load
;             ^^^ meta.function-call - meta.function-call.arguments
;                ^^^^^^^^^^^^^^^^ meta.function-call.arguments
;                                ^ - meta.function-call
;   ^^^ variable.other
;      ^ punctuation.accessor.parameters
;       ^^^ entity.other.attribute-name
;           ^ keyword.operator.assignment
;             ^^^ support.function
;                ^ punctuation.section.parens.begin
;                  ^ punctuation.definition.string.begin
;                  ^^^^^^^^^^^^ string.quoted.double
;                             ^ punctuation.definition.string.end
;                               ^ punctuation.section.parens.end
    CALL("function")
;  ^ - meta.function-call
;   ^^^^ meta.function-call
;       ^^^^^^^^^^^^ meta.function-call.arguments
;                   ^ - meta.function-call
;   ^^^^ support.function
;       ^ punctuation.section.parens.begin
;        ^ punctuation.definition.string.begin
;        ^^^^^^^^^^ string.quoted.double
;                 ^ punctuation.definition.string.end
;                  ^ punctuation.section.parens.end

; IF ELSE CONTROL STRUCTURE TEST
    IF FOO == FALSE
;   ^^ keyword.control.flow.conditional
;      ^^^ variable.other
;          ^^ keyword.operator.relational
;             ^^^^^ constant.language.boolean
      BAR.val = 10
;     ^^^ variable.other
;        ^ punctuation.accessor.parameters
;         ^^^ entity.other.attribute-name
;             ^ keyword.operator.assignment
;               ^^ constant.numeric.integer
    ELSE
;   ^^^^ keyword.control.flow.conditional
      BAR.val = 10
;     ^^^ variable.other
;        ^ punctuation.accessor.parameters
;         ^^^ entity.other.attribute-name
;             ^ keyword.operator.assignment
;               ^^ constant.numeric.integer
    ENDIF
;   ^^^^^ keyword.control.flow.conditional

; DO WHILE CONTROL STRUCTURE TEST
    DO_WHILE FOO.vld
;   ^^^^^^^^ keyword.control.flow.loop
;            ^^^ variable.other
;               ^ punctuation.accessor.parameters
;                ^^^ entity.other.attribute-name
      BAR.val = 10
;     ^^^ variable.other
;        ^ punctuation.accessor.parameters
;         ^^^ entity.other.attribute-name
;             ^ keyword.operator.assignment
;               ^^ constant.numeric.integer
    LOOP
;   ^^^^ keyword.control.flow.loop

; DO UNTIL CONTROL STRUCTURE TEST
    DO_UNTIL NOT FOO.vld
;   ^^^^^^^^ keyword.control.flow.loop
;            ^^^ keyword.operator.logical
;                ^^^ variable.other
;                   ^ punctuation.accessor.parameters
;                    ^^^ entity.other.attribute-name
      BAR.val = 10
;     ^^^ variable.other
;        ^ punctuation.accessor.parameters
;         ^^^ entity.other.attribute-name
;             ^ keyword.operator.assignment
;               ^^ constant.numeric.integer
    LOOP
;   ^^^^ keyword.control.flow.loop

; SWITCH CASE CONTROL STRUCTURE TEST
    SWITCH (FOO)
;          ^^^^^ meta.group
;   ^^^^^^ keyword.control.flow.conditional
;          ^ punctuation.section.group.begin
;           ^^^ variable.other
;              ^ punctuation.section.group.end
    CASE 1
;   ^^^^ keyword.control.flow.conditional
;        ^ constant.numeric.integer
        BAR.val = 10
;       ^^^ variable.other
;          ^ punctuation.accessor.parameters
;           ^^^ entity.other.attribute-name
;               ^ keyword.operator.assignment
;                 ^^ constant.numeric.integer
    DEFAULT
;   ^^^^^^^ keyword.control.flow.conditional
        BAR.val = 50
;       ^^^ variable.other
;          ^ punctuation.accessor.parameters
;           ^^^ entity.other.attribute-name
;               ^ keyword.operator.assignment
;                 ^^ constant.numeric.integer
    END_SWITCH
;   ^^^^^^^^^^ keyword.control.flow.conditional
END_LOAD
; <- meta.class.dialog.body keyword.declaration.function.load.end
;^^^^^^^ meta.class.dialog.body keyword.declaration.function.load.end

UNLOAD
; <- meta.class.dialog.body keyword.declaration.function.unload.begin
;^^^^^ meta.class.dialog.body keyword.declaration.function.unload.begin
    LM("MASK")
;<- meta.class.dialog.body meta.block.method.unload
;^^^^^^^^^^^^^^^ meta.class.dialog.body meta.block.method.unload
;   ^^ meta.function-call
;     ^^^^^^^^ meta.function-call.arguments
;   ^^ support.function
END_UNLOAD
; <- meta.class.dialog.body keyword.declaration.function.unload.end
;^^^^^^^^^ meta.class.dialog.body keyword.declaration.function.unload.end

OUTPUT(output_name, 1)
; <- meta.class.dialog.body keyword.declaration.function.output.begin
;^^^^^^^^^^^^^^^^^^^^^^ meta.class.dialog.body
;     ^^^^^^^^^^^^ meta.function.parameters.output.name
;                  ^^^ meta.function.parameters.output.version
;^^^^^ keyword.declaration.function.output.begin
;     ^ punctuation.section.parameters.begin
;      ^^^^^^^^^^^ string.unquoted entity.name.function.output
;                 ^ punctuation.separator
;                   ^ constant.numeric.integer
;                    ^ punctuation.section.parameters.end
   "CYCLE(""" FOO """," BAR "," BAZ ")"
; <- meta.class.dialog.body meta.block.method.output
;^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ meta.class.dialog.body meta.block.method.output
;  ^^^^^^^^^^ string.quoted.double
;             ^^^ variable.other
;                 ^^^^^ string.quoted.double
;                       ^^^ variable.other
;                           ^^^ string.quoted.double
;                               ^^^ variable.other
;                                   ^^^ string.quoted.double
END_OUTPUT
; <- meta.class.dialog.body keyword.declaration.function.output.end
;^^^^^^^^^ meta.class.dialog.body keyword.declaration.function.output.end

PRESS(ENTER)
; <- meta.class.dialog.body keyword.declaration.function.press.begin
;^^^^^^^^^^^^ meta.class.dialog.body
;    ^^^^^^^ meta.function.parameters.press.softkey
;^^^^ keyword.declaration.function.press.begin
;    ^ punctuation.section.parameters.begin
;     ^^^^^ entity.name.key
;          ^ punctuation.section.parameters.end
    LM("MASK")
;<- meta.class.dialog.body meta.block.method.press
;^^^^^^^^^^^^^^^ meta.class.dialog.body meta.block.method.press
;   ^^ meta.function-call
;     ^^^^^^^^ meta.function-call.arguments
;   ^^ support.function
END_PRESS
; <- meta.class.dialog.body keyword.declaration.function.press.end
;^^^^^^^^ meta.class.dialog.body keyword.declaration.function.press.end

RESOLUTION
; <- meta.class.dialog.body keyword.declaration.function.resolution.begin
;^^^^^^^^^ meta.class.dialog.body keyword.declaration.function.resolution.begin
    LM("MASK")
;<- meta.class.dialog.body meta.block.method.resolution
;^^^^^^^^^^^^^^^ meta.class.dialog.body meta.block.method.resolution
;   ^^ meta.function-call
;     ^^^^^^^^ meta.function-call.arguments
;   ^^ support.function
END_RESOLUTION
; <- meta.class.dialog.body keyword.declaration.function.resolution.end
;^^^^^^^^^^^^^ meta.class.dialog.body keyword.declaration.function.resolution.end

RESUME
; <- meta.class.dialog.body keyword.declaration.function.resume.begin
;^^^^^ meta.class.dialog.body keyword.declaration.function.resume.begin
    LM("MASK")
;<- meta.class.dialog.body meta.block.method.resume
;^^^^^^^^^^^^^^^ meta.class.dialog.body meta.block.method.resume
;   ^^ meta.function-call
;     ^^^^^^^^ meta.function-call.arguments
;   ^^ support.function
END_RESUME
; <- meta.class.dialog.body keyword.declaration.function.resume.end
;^^^^^^^^^ meta.class.dialog.body keyword.declaration.function.resume.end

SUB
;<- meta.method.sub.s840d_hmi keyword.declaration.method.begin.s840d_hmi
;^^ meta.method.sub.s840d_hmi keyword.declaration.method.begin.s840d_hmi
;  ^ meta.method.sub.s840d_hmi

SUB(
;<- meta.method.sub.s840d_hmi keyword.declaration.method.begin.s840d_hmi
;^^ meta.method.sub.s840d_hmi keyword.declaration.method.begin.s840d_hmi
;  ^^ meta.method.sub.parameters.s840d_hmi meta.parens.s840d_hmi
;  ^ punctuation.section.parens.begin.s840d_hmi

SUB(sub_name illegal ; comment
;<- meta.method.sub.s840d_hmi keyword.declaration.method.begin.s840d_hmi
;^^ meta.method.sub.s840d_hmi keyword.declaration.method.begin.s840d_hmi
;  ^^^^^^^^^^^^^^^^^^ meta.method.sub.parameters.s840d_hmi meta.parens.s840d_hmi
;                    ^^^^^^^^^^ meta.method.sub.s840d_hmi
;  ^ punctuation.section.parens.begin.s840d_hmi
;   ^^^^^^^^ entity.name.function.s840d_hmi
;            ^^^^^^^ invalid.illegal.s840d_hmi
;                    ^^^^^^^^^^ comment.line.s840d_hmi

SUB)
;<- meta.method.sub.s840d_hmi keyword.declaration.method.begin.s840d_hmi
;^^ meta.method.sub.s840d_hmi keyword.declaration.method.begin.s840d_hmi
;  ^^ meta.method.sub.s840d_hmi
;  ^ invalid.illegal.s840d_hmi

SUB(sub_name illegal) illegal ; comment
;<- meta.method.sub.s840d_hmi keyword.declaration.method.begin.s840d_hmi
;^^ meta.method.sub.s840d_hmi keyword.declaration.method.begin.s840d_hmi
;  ^^^^^^^^^^^^^^^^^^ meta.method.sub.parameters.s840d_hmi meta.parens.s840d_hmi
;  ^ punctuation.section.parens.begin.s840d_hmi
;   ^^^^^^^^ entity.name.function.s840d_hmi
;            ^^^^^^^ invalid.illegal.s840d_hmi
;                   ^ punctuation.section.parens.end.s840d_hmi
;                     ^^^^^^^ invalid.illegal.s840d_hmi
;                             ^^^^^^^^^^ comment.line.s840d_hmi

SUB(sub_name)
;<- meta.method.sub.s840d_hmi keyword.declaration.method.begin.s840d_hmi
;^^ meta.method.sub.s840d_hmi keyword.declaration.method.begin.s840d_hmi
;  ^^^^^^^^^^ meta.method.sub.parameters.s840d_hmi meta.parens.s840d_hmi
;^^ keyword.declaration.method.begin.s840d_hmi
;  ^ punctuation.section.parens.begin.s840d_hmi
;   ^^^^^^^^ entity.name.function.s840d_hmi
;           ^ punctuation.section.parens.end.s840d_hmi
    LM("MASK")
;<- meta.method.sub.s840d_hmi meta.block.s840d_hmi
;^^^^^^^^^^^^^^ meta.method.sub.s840d_hmi meta.block.s840d_hmi
;   ^^ meta.function-call.identifier.s840d_hmi
;     ^^^^^^^^ meta.function-call.arguments.s840d_hmi
;   ^^ support.function.s840d_hmi
END_SUB
;<- meta.method.sub.s840d_hmi keyword.declaration.method.end.s840d_hmi
;^^^^^^ meta.method.sub.s840d_hmi keyword.declaration.method.end.s840d_hmi
;      ^ - meta.method.sub

SUSPEND
;<- meta.method.s840d_hmi keyword.declaration.method.begin.s840d_hmi
;^^^^^^ meta.method.s840d_hmi keyword.declaration.method.begin.s840d_hmi
;      ^ meta.method.s840d_hmi - keyword

SUSPEND()
;<- meta.method.s840d_hmi keyword.declaration.method.begin.s840d_hmi
;^^^^^^ meta.method.s840d_hmi keyword.declaration.method.begin.s840d_hmi
;      ^^ meta.method.s840d_hmi invalid.illegal.s840d_hmi
;        ^ meta.method.s840d_hmi - keyword - illegal

SUSPEND ; comment
;<- meta.method.s840d_hmi keyword.declaration.method.begin.s840d_hmi
;^^^^^^ meta.method.s840d_hmi keyword.declaration.method.begin.s840d_hmi
;      ^ meta.method.s840d_hmi - keyword - comment
;       ^^^^^^^^^^ meta.method.s840d_hmi comment.line.s840d_hmi

SUSPEND
;<- meta.method.s840d_hmi keyword.declaration.method.begin.s840d_hmi
;^^^^^^ meta.method.s840d_hmi keyword.declaration.method.begin.s840d_hmi
;      ^ meta.method.s840d_hmi - keyword
    LM("MASK")
;<- meta.method.s840d_hmi meta.block.s840d_hmi
;^^^^^^^^^^^^^^ meta.method.s840d_hmi meta.block.s840d_hmi
;   ^^ meta.function-call.identifier.s840d_hmi
;     ^^^^^^^^ meta.function-call.arguments.s840d_hmi
;   ^^ support.function.s840d_hmi
END_SUSPEND
;<- meta.method.s840d_hmi keyword.declaration.method.end.s840d_hmi
;^^^^^^^^^^ meta.method.s840d_hmi keyword.declaration.method.end.s840d_hmi
;          ^ - meta.method

//END    ; //M(NAME)
; <- meta.class.dialog.s840d_hmi keyword.declaration.class.end.s840d_hmi
;^^^^ meta.class.dialog.s840d_hmi keyword.declaration.class.end.s840d_hmi
;    ^^^^^^^^^^^^^^^ - meta.class
;        ^^^^^^^^^^^ comment.line

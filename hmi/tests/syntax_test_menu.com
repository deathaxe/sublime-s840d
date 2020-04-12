; SYNTAX TEST "s840d_hmi.sublime-syntax"

; ==================================================
;  //S tests
;  Performance: 0.1ms
; ==================================================

//S(MNU_NAME, "translate1.txt", "translate2.txt"/)
;^^ meta.class.menu keyword.declaration.class.begin
;  ^ meta.class.menu.parameters.name punctuation.section.parameters.begin
;   ^^^^^^^^ meta.class.menu.parameters.name entity.name.class
;           ^ meta.class.menu.parameters.name punctuation.separator.parameters
;             ^^^^^^^^^^^^^^^^ meta.class.menu.parameters.langfiles string.quoted.double
;                             ^ meta.class.menu.parameters.langfiles punctuation.separator
;                               ^^^^^^^^^^^^^^^^ meta.class.menu.parameters.langfiles string.quoted.double
;                                               ^ meta.class.menu.parameters.langfiles invalid.illegal.separator
;                                                ^ meta.class.menu.parameters punctuation.section.parameters.end - meta.class.menu.parameters.langfiles
//END
;<- meta.class.menu.end keyword.declaration.class.end
;^^^^ meta.class.menu.end keyword.declaration.class.end

//S(MNU_NAME)
;^^ meta.class.menu keyword.declaration.class.begin
;  ^ meta.class.menu.parameters.name punctuation.section.parameters.begin
;   ^^^^^^^^ meta.class.menu.parameters.name entity.name.class
;           ^ meta.class.menu.parameters punctuation.section.parameters.end - meta.class.menu.parameters.langfiles
//END
;<- meta.class.menu.end keyword.declaration.class.end
;^^^^ meta.class.menu.end keyword.declaration.class.end

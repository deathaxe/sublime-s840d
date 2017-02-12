; SYNTAX TEST "s840d_hmi.sublime-syntax"

; ==================================================
;  //B tests
;  Performance: 0.5ms
; ==================================================

//B(BLOCK_NAME)
;              <- meta.class.subprogram
;   ^^^^^^^^^^ meta.parens
;  <- keyword.class.begin
;  ^ punctuation.section.parens.begin
;   ^^^^^^^^^^ entity.name.class
;             ^ punctuation.section.parens.end

SUB(SUB_NAME)

END_SUB


//END
;    <- meta.class.subprogram.end
;    <- keyword.class.end

<?php

interface IPPCode
{
    // Frame and Function Calls Instructions
    const HEADER        = ".IPPcode21";
    const MOVE          = "MOVE";
    const CREATEFRAME   = "CREATEFRAME";
    const PUSHFRAME     = "PUSHFRAME";
    const POPFRAME      = "POPFRAME";
    const DEFVAR        = "DEFVAR";
    const CALL          = "CALL";
    const RETURN        = "RETURN";

    // Data Stack Instructions
    const PUSHS         = "PUSHS";
    const POPS          = "POPS";

    // Arithmetic, Relation, Boolean, and Conversion Intstructions
    const ADD           = "ADD";
    const SUB           = "SUB";
    const MUL           = "MULL";
    const IDIV          = "IDIV";
    const LT            = "LT";
    const GT            = "GT";
    const EQ            = "EQ";
    const AND           = "AND";
    const OR            = "OR";
    const NOT           = "NOT";
    const INT2CHAR      = "INT2CHAR";
    const STRI2INT      = "STRI2INT";

    // Input, Output Instructions
    const READ          = "READ";
    const WRITE         = "WRITE";

    // String Instructions
    const CONCAT        = "CONCAT";
    const STRLEN        = "STRLEN";
    const GETCHAR       = "GETCHAR";
    const SETCHAR       = "SETCHAR";

    // Type Instructions
    const TYPE          = "TYPE";

    // Flow Instructions
    const LABEL         = "LABEL";
    const JUMP          = "JUMP";
    const JUMPIFEQ      = "JUMPIFEQ";
    const JUMPIFNEQ     = "JUMPIFNEQ";
    const EXIT          = "EXIT";

    // Debugging Instructions
    const DPRINT        = "DPRINT";
    const BREAK         = "BREAK";
}
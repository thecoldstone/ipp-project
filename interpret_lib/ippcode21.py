class IppCode21:
    instructions = [
        "MOVE",
        "CREATEFRAME",
        "PUSHFRAME",
        "POPFRAME",
        "DEFVAR",
        "CALL",
        "RETURN",
        # Data Stack Instructions
        "PUSHS",
        "POPS",
        # Arithmetic, Relation, Boolean, and Conversion Intstructions
        "ADD",
        "SUB",
        "MUL",
        "IDIV",
        "LT",
        "GT",
        "EQ",
        "AND",
        "OR",
        "NOT",
        "INT2CHAR",
        "STRI2INT",
        # Input, Output Instructions
        "READ",
        "WRITE",
        # String Instructions
        "CONCAT",
        "STRLEN",
        "GETCHAR",
        "SETCHAR",
        # Type Instructions
        "TYPE",
        # Flow Instructions
        "LABEL",
        "JUMP",
        "JUMPIFEQ" "JUMPIFNEQ",
        "EXIT",
        # Debugging Instructions
        "DPRINT",
        "BREAK",
    ]
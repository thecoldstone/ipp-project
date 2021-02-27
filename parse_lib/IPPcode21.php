<?php

interface IPPCode
{
    const HEADER        = ".IPPcode21";
    const MOVE          = "MOVE";
    const CREATEFRAME   = "CREATEFRAME";
    const PUSHFRAME     = "PUSHFRAME";
    const POPFRAME      = "POPFRAME";
    const DEFVAR        = "DEFVAR";
    const CALL          = "CALL";
    const RETURN        = "RETURN";
}
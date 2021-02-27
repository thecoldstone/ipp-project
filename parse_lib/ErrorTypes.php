<?php

interface ErrorTypes
{
    const OK                    = 0;
    const BADPARAMETER          = 10;
    const ERRORINPUTFILE        = 11;
    const ERROROUTPUTFILE       = 12;
    const MISSINGHEADER         = 21;
    const FOREIGNOPCODE         = 22;
    const LEXSYNTAXERROR        = 23;
    const INTERNALERROR         = 99;
}
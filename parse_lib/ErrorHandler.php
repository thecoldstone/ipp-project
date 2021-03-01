<?php

class ErrorHandler {

    protected $parserState = ErrorTypes::OK;

    public function check_tockens($expected, $actual)
    {
        if($expected != $actual) {
            fprintf(STDERR, "[ERROR] Number of tockens is incorrect");
            $this->parserState = ErrorTypes::LEXSYNTAXERROR;
        }
    }

    public function exit_program($text, $error_status, $line_number) 
    {
        fprintf(STDERR, "[ERROR] ".$text." on a line {$line_number}");
        exit($error_status);
    }
}
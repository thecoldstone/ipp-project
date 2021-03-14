<?php

class ErrorHandler {

    // TODO Refactoring
    // Use raise Error and Try & Catch in parse.php

    protected $parserState = ErrorTypes::OK;
    protected $currentLine;

    public function check_tockens($expected, $actual)
    {
        if($expected != $actual) {
            $this->exit_program("Number of tockens is incorrect", ErrorTypes::LEXSYNTAXERROR);
        }
    }

    public function exit_program($text, $error_status) 
    {
        fprintf(STDERR, "[ERROR] ".$text." on a line {$this->currentLine}\n");
        exit($error_status);
    }
}
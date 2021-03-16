<?php

class ErrorHandler {

    // TODO Refactoring
    // Use raise Error and Try & Catch in parse.php
    
    protected $currentLine;

    public function exit_program($text, $error_status) 
    {
        fprintf(STDERR, "[ERROR] ".$text." on a line {$this->currentLine}\n");
        exit($error_status);
    }
}
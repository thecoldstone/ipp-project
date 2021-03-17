<?php
/**
 * Project : Parser implementation for IPPCode21
 * 
 * Class of error handling
 * 
 * @author Nikita Zhukov
 * @todo Enrich error handler with raise statement (add try/catch logic)
 */
class ErrorHandler {
    
    protected $currentLine;

    /**
     * @param $text Error text
     * @param $error_status Status of error to exit the program
     */
    public function exit_program($text, $error_status) 
    {
        fprintf(STDERR, "[ERROR] ".$text." on a line {$this->currentLine}\n");
        exit($error_status);
    }
}
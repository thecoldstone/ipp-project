<?php

require "ErrorHandler.php";
require "IPPcode21.php";

class Parser extends ErrorHandler
{
    private $stats;
    private $currentInstruction;
    private $currentArguments;
    private $headerFlag;

    public function __construct(Stats $stats)
    {
        $this->stats = $stats;
        $this->currentArguments = array();
        $this->headerFlag = false;
    }

    private function load_instruction()
    {
        if(!($line = fgets(STDIN))) {
            return -1;
        } 

        # Remove comment whether it appears
        $line = $this->check_comment($line);

        # Omit redundant spaces
        $line = preg_replace("/\s+/", ' ', $line);
        $line = trim($line);

        $tockens = explode(' ', $line);

        $this->stats->cntLines++;

        return $tockens;
    }

    public function parse()
    {
        // TODO Enable reading blank lines at the beginning of the file
        while (($tockens = $this->load_instruction()) != -1) {

            # Check the header whether it has already appeared
            if(!$this->headerFlag && count($tockens) > 0) {

                # Once there is just a blank line we can continue the parsing
                if(empty($tockens[0])) {
                    continue;
                }

                # Otherwise check the content of this line
                if(!$this->check_header($tockens[0])) {
                    $this->exit_program(".IPPcode21 header is missing", ErrorTypes::MISSINGHEADER, $this->stats->cntLines);
                }

                # Once everything has passed successfully the program can keep going the parsing
                continue;
            }

            # Check the syntax of the instruction
            $this->check_syntax($tockens);
        }
    }

    public function check_syntax($tockens) 
    {
        switch (strtoupper($tockens[0])) {
            case IPPCode::MOVE: // MOVE <var> <symb>
                $this->check_tockens(3, count($tockens));
                $this->check_var($tockens[1]);      // <var>
                $this->check_symbol($tockens[2]);   // <symb>

                break;
            case IPPCode::CREATEFRAME:  // CREATFRAME
            case IPPCode::PUSHFRAME:    // PUSHFRAME
            case IPPCode::POPFRAME:     // POPFRAME
            case IPPCode::RETURN:
                $this->check_tockens(1, count($tockens));
                // TODO

                break;
            case IPPCode::DEFVAR: // DEFVAR <var>
                $this->check_tockens(2, count($tockens));
                $this->check_var($tockens[1]);

                break;

            case IPPCode::CALL: // CALL <label>
            case IPPCode::LABEL: // LABEL <label>
            case IPPCode::JUMP: // JUMP <label>
                $this->check_tockens(2, count($tockens));
                $this->check_label($tockens[1]);

                break;

            case IPPCode::JUMPIFEQ:
            case IPPCode::JUMPIFNEQ:
                $this->check_tockens(4, count($tockens));

                break;

            case IPPCode::PUSHS:
            case IPPCode::POPS:
                $this->check_tockens(2, count($tockens));
                $this->check_symbol($tockens[1]);

                break;

            case IPPCode::ADD:
                break;

            case IPPCode::CONCAT:
                $this->check_tockens(4, count($tockens));
                $this->check_var($tockens[1]);
                $this->check_symbol($tockens[2]);
                $this->check_symbol($tockens[3]);

                break;

            case IPPCode::WRITE:
                $this->check_tockens(2, count($tockens));
                $this->check_symbol($tockens[1]);

                break;

            default:
                $this->exit_program("Foreign instruction code {$tockens[0]}", ErrorTypes::FOREIGNOPCODE, $this->stats->cntLines);
        }
    }

    private function check_header($header)
    {
        if ($header == IPPCode::HEADER) {
            $this->headerFlag = true;
            return true;
        } else {
            return false;
        }
    }


    private function check_comment($line)
    {   
        if (strpos($line, "#") !== false) {
            $line = explode("#", $line);
            $this->stats->cntComments++;
            return $line[0];
        }

        return $line;
    }

    private function check_var($var)
    {
        // TODO collect the statistics
        if (preg_match("/^(GF|LF|TF)@(_|-|\$|&|%|\*|\!|\?|[a-zA-Z])(_|-|\$|&|%|\*|\!|\?|[a-zA-Z0-9])*$/", $var)) {
            array_push($this->currentArguments, ['var' => $var]);
        } else {
            $this->exit_program(".IPPcode21 header is missing\n", ErrorTypes::MISSINGHEADER, $this->stats->cntLines);
        }
    }

    private function check_label($label)
    {
        // TODO collect the statistics
        if (preg_match("/^(_|-|\$|&|%|\*|\!|\?|[a-zA-Z])(_|-|\$|&|%|\*|\!|\?|[a-zA-Z0-9])*$/", $label)) {
            array_push($this->currentArguments, ['label' => $label]);
        } else {
            $this->exit_program(".IPPcode21 header is missing\n", ErrorTypes::MISSINGHEADER, $this->stats->cntLines);
        }
    }

    private function check_symbol($symbol)
    {
        if (preg_match("/^(int|bool|string)@.*$/", $symbol)) {
            $symbol = explode("@", $symbol, 2);
            switch ($symbol[0]) {
                case "int":
                    if (empty($symbol[1])) {
                        $this->exit_program(
                            "Missing value for integer\n",
                            ErrorTypes::LEXSYNTAXERROR, $this->stats->cntLines
                        );
                    }
                    array_push($this->currentArguments, [$symbol[0] => $symbol[1]]);
                    break;
                case "bool":
                    if (!preg_match("/^(true|false)$/", $symbol[1])) {
                        $this->exit_program(
                            "Missing value for integer\n",
                            ErrorTypes::LEXSYNTAXERROR, $this->stats->cntLines
                        );
                    }
                    array_push($this->currentArguments, [$symbol[0] => $symbol[1]]);
                    break;
                case "string":
                    array_push($this->currentArguments, [$symbol[0] => $symbol[1]]);
                    break;
            }
        } else if(preg_match("/^(GF|LF|TF)@.*$/", $symbol)) {
            // TODO Check the case GF@<empty>
            $this->check_var($symbol);
        } else {
            $this->exit_program(
                "Syntax Error",
                ErrorTypes::LEXSYNTAXERROR, $this->stats->cntLines
            );
        }
    }

    private function check_type($type)
    {
        // TODO
    }
}

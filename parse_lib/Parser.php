<?php

require "DOMWriter.php";
require "parserInitHandler.php";
require "ErrorHandler.php";
require "ErrorTypes.php";
require "IPPcode21.php";

class Parser extends ErrorHandler
{
    use parserInitHandler;

    private $currentInstruction;
    private $currentArguments;
    private $headerFlag;

    private $dom;

    public function __construct()
    {
        $this->init_parser();

        $this->currentArguments = array();
        $this->headerFlag = false;

        $this->dom = new DOMWriter();
    }

    private function load_instruction()
    {
        if (!($line = fgets(STDIN))) {
            return false;
        }

        # Remove comment whether it appears
        $line = $this->check_comment($line);

        # Omit redundant spaces
        $line = preg_replace("/\s+/", ' ', $line);
        $line = trim($line);

        $tockens = explode(' ', $line);

        $this->stats->addUpLine();

        return $tockens;
    }

    public function parse()
    {
        while (($tockens = $this->load_instruction())) {

            # If the line contains the comment or it's empty
            if (empty($tockens[0])) {
                continue;
            }

            # Check the header whether it has already appeared
            if (!$this->headerFlag && count($tockens) > 0) {

                # Once there is just a blank line we can continue the parsing
                if (empty($tockens[0])) {
                    continue;
                }

                # Otherwise check the content of this line
                if (!$this->check_header($tockens[0])) {
                    $this->exit_program(".IPPcode21 header is missing", ErrorTypes::MISSINGHEADER, $this->stats->cntLines);
                }

                # Once everything has passed successfully the program can keep going the parsing
                continue;
            }

            # Check the syntax of the instruction
            $this->check_syntax($tockens);

            # Write to XML file
            $this->dom->set_instruction($this->stats->getInstruction(), $this->currentInstruction, $this->currentArguments);
        }

        $this->write_to_files();
        $this->dom->save();
    }

    private function check_syntax($tockens)
    {
        $this->currentInstruction = strtoupper($tockens[0]);
        $this->currentArguments = [];
        $this->stats->addUpInstruction();

        switch ($this->currentInstruction) {
            case IPPCode::MOVE: // <var> <symb>
            case IPPCode::INT2CHAR:
            case IPPCode::STRLEN:
            case IPPCode::TYPE:
                $this->check_tockens(3, count($tockens));
                $this->check_var($tockens[1]);
                $this->check_symbol($tockens[2]);

                break;
            case IPPCode::CREATEFRAME:
            case IPPCode::PUSHFRAME:
            case IPPCode::POPFRAME:
            case IPPCode::RETURN:
            case IPPCode::BREAK:
                $this->check_tockens(1, count($tockens));
                $this->check_brake($tockens[0]);

                if ($this->currentInstruction == IPPCode::RETURN) {
                    $this->stats->addUpJump();
                }

                break;
            case IPPCode::DEFVAR: // <var>
            case IPPCode::POPS:
                $this->check_tockens(2, count($tockens));
                $this->check_var($tockens[1]);

                break;

            case IPPCode::CALL: // <label>
            case IPPCode::LABEL:
            case IPPCode::JUMP:
                $this->check_tockens(2, count($tockens));
                $this->check_label($tockens[1]);
                if ($this->currentInstruction == IPPCode::LABEL) {
                    $this->stats->check_label($tockens[1]);
                } else {
                    $this->stats->addUpJump();
                }

                break;

            case IPPCode::JUMPIFEQ: // <label> <symb1> <symb2>
            case IPPCode::JUMPIFNEQ:
                $this->check_tockens(4, count($tockens));
                $this->check_label($tockens[1]);
                $this->check_symbol($tockens[2]);
                $this->check_symbol($tockens[3]);
                $this->stats->addUpJump();

                break;

            case IPPCode::PUSHS: // <symb>
            case IPPCode::WRITE:
            case IPPCode::EXIT:
            case IPPCode::DPRINT:
                $this->check_tockens(2, count($tockens));
                $this->check_symbol($tockens[1]);
                $this->check_dprint($tockens);

                break;

            case IPPCode::ADD: // <var> <symb1> <symb2>
            case IPPCode::SUB:
            case IPPCode::MUL:
            case IPPCode::IDIV:
            case IPPCode::LT:
            case IPPCode::GT:
            case IPPCode::EQ:
            case IPPCode::AND:
            case IPPCode::OR:
            case IPPCode::NOT:
            case IPPCode::STRI2INT:
            case IPPCode::CONCAT:
            case IPPCode::GETCHAR:
            case IPPCode::SETCHAR:
                $this->check_tockens(4, count($tockens));
                $this->check_var($tockens[1]);
                $this->check_symbol($tockens[2]);
                $this->check_symbol($tockens[3]);

                break;

            case IPPCode::READ: // READ <var> <type>
                $this->check_tockens(3, count($tockens));
                $this->check_var($tockens[1]);
                $this->check_type($tockens[2]);

                break;

            default:
                $this->exit_program("Foreign instruction code {$tockens[0]}", ErrorTypes::FOREIGNOPCODE, $this->stats->getLine());
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
            $this->stats->addUpComment();
            return $line[0];
        }

        return $line;
    }

    private function check_var($var)
    {
        // TODO collect the statistics
        if (preg_match("/^(GF|LF|TF)@(_|-|\$|&|%|\*|\!|\?|[a-zA-Z])(_|-|\$|&|%|\*|\!|\?|[a-zA-Z0-9])*$/", $var)) {
            array_push($this->currentArguments, ["var" => $var]);
        } else {
            $this->exit_program(".IPPcode21 header is missing\n", ErrorTypes::MISSINGHEADER, $this->stats->getLine());
        }
    }

    private function check_label($label)
    {
        // TODO collect the statistics
        if (preg_match("/^(_|-|\$|&|%|\*|\!|\?|[a-zA-Z])(_|-|\$|&|%|\*|\!|\?|[a-zA-Z0-9])*$/", $label)) {
            array_push($this->currentArguments, ["label" => $label]);
        } else {
            $this->exit_program(".IPPcode21 header is missing\n", ErrorTypes::MISSINGHEADER, $this->stats->getLine());
        }
    }

    private function check_symbol($symbol)
    {
        if (preg_match("/^(int|bool|string|nil|float)@.*$/", $symbol)) {
            $symbol = explode("@", $symbol, 2);
            switch ($symbol[0]) {
                case "int":
                    if (strlen($symbol[1]) == 0) {
                        $this->exit_program(
                            "Missing value for integer\n",
                            ErrorTypes::LEXSYNTAXERROR,
                            $this->stats->getLine()
                        );
                    }
                    array_push($this->currentArguments, ["int" => $symbol[1]]);
                    break;

                case "bool":
                    if (!preg_match("/^(true|false)$/", $symbol[1])) {
                        $this->exit_program(
                            "Incorrect boolean type {$symbol[1]}\n",
                            ErrorTypes::LEXSYNTAXERROR,
                            $this->stats->getLine()
                        );
                    }
                    array_push($this->currentArguments, ["bool" => $symbol[1]]);
                    break;

                case "string":
                    array_push($this->currentArguments, ["string" => $symbol[1]]);
                    break;

                case "nil":
                    if (!preg_match("/^(nil)$/", $symbol[1])) {
                        $this->exit_program(
                            "Incorrect nil type {$symbol[1]}\n",
                            ErrorTypes::LEXSYNTAXERROR,
                            $this->stats->getLine()
                        );
                    }
                    array_push($this->currentArguments, ["nil" => $symbol[1]]);
                    break;

                case "float":
                    if (strlen($symbol[1]) == 0) {
                        $this->exit_program(
                            "Missing value for float\n",
                            ErrorTypes::LEXSYNTAXERROR,
                            $this->stats->getLine()
                        );
                    }
                    array_push($this->currentArguments, ["float" => $symbol[1]]);
                    break;
            }
        } else if (preg_match("/^(GF|LF|TF)@.*$/", $symbol)) {
            // TODO Check the case GF@<empty>
            $this->check_var($symbol);
        } else {
            $this->exit_program("Syntax Error", ErrorTypes::LEXSYNTAXERROR, $this->stats->getLine());
        }
    }

    private function check_type($type)
    {
        if (preg_match("/^(int|bool|string|float)$/", $type)) {
            array_push($this->currentArguments, ["type" => $type]);
        } else {
            $this->exit_program("Type {$type} does not exist", ErrorTypes::LEXSYNTAXERROR, $this->stats->getLine());
        }
    }

    private function check_dprint($tockens)
    {
        if ($tockens[0] == "DPRINT") {
            fprintf(STDERR, "{$tockens[1]}.\n");
        }
    }

    private function check_brake($tocken)
    {
        if ($tocken == "BREAK") {
            fprintf(
                STDERR,
                "Breakpoint : {$this->stats->getLine()}\nCalled instructions : {$this->stats->getInstruction()}\n"
            );
        }
    }
}

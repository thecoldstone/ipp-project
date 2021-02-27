<?php

require "IPPcode21.php";

class Parser
{
    private $stats;
    private $currentInstruction;
    private $currentArguments;

    public function __construct(Stats $stats)
    {
        $this->stats = $stats;
        $this->currentArguments = array();
    }

    public function load_instruction()
    {
        $line = fgets(STDIN);

        # Omit redundant spaces
        $line = preg_replace("/\s+/", ' ', $line);
        $line = trim($line);

        $tockens = explode(' ', $line);

        $this->stats->cntLines++;

        return $tockens;
    }

    public function has_header()
    {
        $line = $this->load_instruction();

        if ($line[0] == IPPCode::HEADER) {
            return true;
        } else {
            return false;
        }
    }

    public function parse()
    {
        if (!$this->has_header()) {
            fprintf(STDERR, ".IPPcode21 header is missing\n");
            exit(ErrorTypes::MISSINGHEADER);
        }

        $status = ErrorTypes::OK;

        while ($status == ErrorTypes::OK) {

            $tockens = $this->load_instruction();

            switch (strtoupper($tockens[0])) {
                case IPPCode::MOVE: // MOVE <var> <symb>
                    if (count($tockens) == 3) {
                    } else {
                        exit(ErrorTypes::LEXSYNTAXERROR);
                    }
                    break;
                case IPPCode::CREATEFRAME:
                case IPPCode::PUSHFRAME:
                case IPPCode::POPFRAME:
                    if (count($tockens) == 1) {
                        // TODO
                    } else {
                        exit(ErrorTypes::LEXSYNTAXERROR);
                    }
                    break;
                case IPPCode::DEFVAR: // DEFVAR <var>
                    if (count($tockens) == 2) {
                        if (!$this->is_var($tockens[1])) {
                            exit(ErrorTypes::LEXSYNTAXERROR);
                        }
                    } else {
                        exit(ErrorTypes::LEXSYNTAXERROR);
                    }
                    break;
                default:
                    exit(ErrorTypes::FOREIGNOPCODE);
            }
        }
    }

    public function is_var($var)
    {
        if (preg_match("/^(GF|LF|TF)@([a-zA-Z0-9]*)$/", $var)) {
            array_push($this->currentArguments, ['var' => $var]);
        } else {
            return false;
        }
    }

    public function is_label($label)
    {
        // TODO
    }

    public function is_symbol($symbol)
    {
        // TODO
    }

    public function is_type($type)
    {
        // TODO
    }
}

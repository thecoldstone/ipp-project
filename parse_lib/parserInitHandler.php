<?php

require "Stats.php";

trait parserInitHandler
{
    protected $stats;
    protected $file;

    protected $flgStats;

    public function usage()
    {
        echo "Usage of parser.php:\n";
        echo "\t-h, --help              Show the usage.\n";
        echo "\t-s=FILE, --stats=FILE   Enable the collection of statistics.\n";

        echo "In order to store statistics the following flags are mandatory:\n";
        echo "\t--loc                   Count of rows with instructions.\n";
        echo "\t--comments              Count of rows with comments.\n";
        echo "\t--labels                Count of rows with jumps/callbacks.\n";
        echo "\t--\n";
    }

    protected function init_parser()
    {
        // TODO Refactoring 
        $this->stats = new Stats();
        $this->flgStats = false;

        // Parse arguments 
        global $argc, $argv;
        $optind = 0;
        $shortopts = "hs:";
        $longopts  = array("help", "stats:", "loc", "comments", "labels");

        $opts = getopt($shortopts, $longopts, $optind);

        if ($argc == 2) {
            if (array_key_exists("help", $opts) || array_key_exists("h", $opts)) {
                $this->usage();
                exit(ErrorTypes::OK);
            } elseif (array_key_exists("stats", $opts) || array_key_exists("s", $opts)) {
                $this->flgStats = true;

                // Set output file for statistics
                foreach ($opts as $key => $value) {
                    $this->file = $value;
                }
            } else {
                fprintf(STDERR, "[ERROR] Wrong combination of flags\n");
                exit(ErrorTypes::BADPARAMETER);
            }
        } elseif ($argc > 2) {

            $loc = false;
            $comments = false;
            $cntFiles = -1;
            $fileNames = array();
            $this->file = array();

            if (array_key_exists("help", $opts) || array_key_exists("h", $opts)) {
                fprintf(STDERR, "[ERROR] -h or --help flag with combination\n");
                exit(ErrorTypes::BADPARAMETER);
            }

            if (!array_key_exists("stats", $opts) && !array_key_exists("s", $opts)) {
                fprintf(STDERR, "[ERROR] -s or --stats flag is missing\n");
                exit(ErrorTypes::BADPARAMETER);
            }
            
            if(!preg_match("/^(--stats|-s)=[a-zA-Z].*/", $argv[1])) {
                fprintf(STDERR, "[ERROR] Wrong combination of flags\n");
            } else {
                $filename = explode('=', $argv[1]);
                $cntFiles++;
                array_push($this->file, ["file" => $filename[1]]);
                array_push($fileNames, $filename[1]);
            }

            for ($i=2; $i < $argc; $i++) {
                
                if(preg_match("/^(--stats|-s)=[a-zA-Z].*/", $argv[$i])) {
                    $filename = explode('=', $argv[$i]);
                    if(in_array($filename[1], $fileNames)) {
                        fprintf(STDERR, "[ERROR] File's name {$filename[1]} repeats\n");
                        exit(ErrorTypes::ERROROUTPUTFILE);
                    }
                    $cntFiles++;
                    array_push($this->file, ["file" => $filename[1]]);
                    array_push($fileNames, $filename[1]);
                } else {
                    if(!preg_match("/^(--loc|--comments|--labels|--jumps|--fwjumps|--backjumps|--badjumps)/", $argv[$i])) {
                        fprintf(STDERR, "[ERROR] Flag {$argv[$i]} does not exist\n");
                        exit(ErrorTypes::BADPARAMETER);
                    }

                    array_push($this->file[$cntFiles], $argv[$i]);
                }
            }
        }

        // var_dump($this->file);

        return $this->stats;
    }

    private function check_filename() 
    {
        // TODO
    }
}

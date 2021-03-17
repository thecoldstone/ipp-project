<?php
/**
 * Project : Parser implementation for IPPCode21
 * 
 * Parser Initialization Handler Trait 
 * 
 * @author Nikita Zhukov
 * @todo Refactoring
 */ 
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
        echo "\t--jumps                 Count of rows with all jumps\n";
    }

    /**
     * Handler for arguments (flags)
     * 
     * @return $stats Initialized logger for statistics 
     */
    protected function init_parser()
    {
        $this->stats = new Stats();
        $this->flgStats = false;

        global $argc, $argv;
        $optind = 0;
        $shortopts = "hs:";
        $longopts  = array("help", "stats:", "loc", "comments", "labels", "jumps", "fwjumps", "backjumps", "badjumps");

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

            $this->flgStats = true;
            
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

        return $this->stats;
    }

    /**
     * @todo
     */
    private function check_filename() 
    {
    }

    /**
     * Write a statistic to the file 
     */
    protected function write_to_files()
    {
        if(!$this->flgStats) {
            return;
        }

        if (!is_array($this->file)) {
            $file = fopen($this->file, "w");
            fclose($file);
        } else {
            foreach($this->file as $key => $f) {
                // var_dump($f);
                $file = fopen($f["file"], "w");
                if(in_array("--loc", $f)) {
                    fwrite($file, "Count of instructions : {$this->stats->getInstruction()}\n");
                }
                if(in_array("--comments", $f)) {
                    fwrite($file, "Count of comments : {$this->stats->getComment()}\n");
                }
                if(in_array("--labels", $f)) {
                    fwrite($file, "Count of labels : {$this->stats->getLabel()}\n");
                }
                if(in_array("--jumps", $f)){
                    // TODO Change to jumps
                    fwrite($file, "Count of jumps : {$this->stats->getLabel()}\n");
                }
                if(in_array("--fwjumps", $f)){
                    // TODO Change to jumps
                    fwrite($file, "Count of fwjumps : {$this->stats->getLabel()}\n");
                }
                if(in_array("--backjumps", $f)){
                    // TODO Change to jumps
                    fwrite($file, "Count of backjumps : {$this->stats->getLabel()}\n");
                }
                if(in_array("--badjumps", $f)){
                    // TODO Change to jumps
                    fwrite($file, "Count of badjumps : {$this->stats->getLabel()}\n");
                }

                fclose($file);
            }
        }
    }
}

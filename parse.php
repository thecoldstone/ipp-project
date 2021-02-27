<?php

require "parse_lib/Stats.php";
require "parse_lib/Parser.php";
require "parse_lib/ErrorTypes.php";

ini_set('display_errors', 'stderr');

function usage()
{
    echo "Usage of parser.php:\n";
    echo "\t-h, --help              Show the usage.\n";
    echo "\t-s=FILE, --stats=FILE   Enable the collection of statistics.\n";
}

$stats = new Stats();
$flgStats = false;
$file;

// Parse arguments 
global $argc;
$shortopts = "hs:lc";
$longopts  = array("help", "stats:", "loc", "comments");

$opts = getopt($shortopts, $longopts);

if($argc == 2) {
    if (array_key_exists("help", $opts) || array_key_exists("h", $opts)) {
        usage();
        return ErrorTypes::OK;
    } elseif (array_key_exists("stats", $opts) || array_key_exists("s", $opts)) {
        $flgStats = true;
    }
} elseif($argc > 2) {
    // Parse the rest
}

$parser = new Parser($stats);
$parser->parse();

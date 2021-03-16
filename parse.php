<?php

/**
 * 
 */

require "parse_lib/Parser.php";

ini_set('display_errors', 'stderr');

$parser = new Parser();
$parser->parse();
<?php
/**
 * Project : Parser implementation for IPPCode21
 * 
 * Example of using parser
 * 
 * @author Nikita Zhukov xzhuko01
 */

require "parse_lib/Parser.php";

ini_set('display_errors', 'stderr');

$parser = new Parser();
$parser->parse();
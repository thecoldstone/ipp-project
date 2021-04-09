<?php

require "test_lib/test.php";

ini_set('display_errors', 'stderr');

$test = new Test();

try {
    if ($argc > 1) {
        $test->parse_args();
    }
    $test->run();
} catch (Exception $e) {
    echo "[ERROR] ", $e->getMessage(), "\n";
    exit($e->getCode());
}

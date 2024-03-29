<?php

require "test_lib/test.php";

$test = new Test();

try {
    if ($argc > 1) {
        $test->parse_args();
    }
    $test->setup();
    $test->run();
} catch (Exception $e) {
    echo "[ERROR] ", $e->getMessage(), "\n";
    exit($e->getCode());
}

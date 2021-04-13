<?php

/**
 * Project : Test Framework for IPPCode21
 * 
 * Test Data for Framework
 * 
 * @author Nikita Zhukov
 */

trait testDataInitializer
{
    protected $test_data = [];

    protected function init_data($path, $recursive)
    {
        $dir = new RecursiveDirectoryIterator($path);
        if ($recursive) {
            $dir_files = new RecursiveIteratorIterator($dir);
        } else {
            $dir_files = new IteratorIterator($dir);
        }

        foreach ($dir_files as $file) {

            # Skip directories
            if (is_dir($file)) {
                continue;
            }

            # Skip if it's not a source file
            if (!preg_match('/(.*\/(.*))\.src/', $file)) {
                continue;
            }

            $cur_file = substr(realpath($file), 0, -3);
            if (!file_exists($cur_file . "in")) {
                $this->create_file($cur_file . "in", "");
            }
            if (!file_exists($cur_file . "out")) {
                $this->create_file($cur_file . "out", "");
            }
            if (!file_exists($cur_file . "rc")) {
                $this->create_file($cur_file . "rc", "0");
            }

            array_push($this->test_data, realpath($file));
        }
    }

    private function create_file($fname, $data = null)
    {
        echo "[NEW FILE] {$fname} has been created...\n";
        file_put_contents($fname, $data);
    }
}

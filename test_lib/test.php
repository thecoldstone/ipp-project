<?php

/**
 * Project : Test Framework for IPPCode21
 * 
 * Test Framework Main File
 * 
 * @author Nikita Zhukov
 */

require "test_lib/argumentHandler.php";

class Test
{
    use argumentHandler;

    private $path;

    public function __construct()
    {
        $this->path = getcwd();
        $this->test_directory = $this->path;
        $this->recursive = false;
        $this->parse_script = $this->path . '/parse.php';
        $this->int_script = $this->path . '/interpret.py';
        $this->parse_only = false;
        $this->int_only = false;
        $this->jexamxml = $this->path . '/pub/courses/ipp/jexamxml/jexamxml.jar';
        $this->jexamcfg = $this->path . '/pub/courses/ipp/jexamxml/options';
    }

    public function run()
    {
        // TODO
    }

    public function build_html()
    {
        // TODO
    }
}

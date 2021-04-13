<?php

/**
 * Project : Test Framework for IPPCode21
 * 
 * Test Framework Main File
 * 
 * @author Nikita Zhukov
 */

require "test_lib/argumentHandler.php";
require "test_lib/testData.php";

class Test
{
    use argumentHandler;
    use testDataInitializer;

    private $path;

    private $JEXAMXML_MERLIN = '/pub/courses/ipp/jexamxml/jexamxml.jar';
    private $JEXAMCFG_MERLIN = '/pub/courses/ipp/jexamxml/options';

    private $JEXAMXML_MAC    = '/jexamxml/jexamxml.jar';
    private $JEXAMCFG_MAC    = '/jexamxml/options';

    public function __construct()
    {
        $this->path = getcwd();
        $this->test_directory = $this->path;
        $this->recursive = false;
        $this->parse_script = $this->path . '/parse.php';
        $this->int_script = $this->path . '/interpret.py';
        $this->parse_only = false;
        $this->int_only = false;
        $this->jexamxml = $this->path . $this->JEXAMXML_MAC;
        $this->jexamcfg = $this->path . $this->JEXAMCFG_MAC;
    }

    public function setup()
    {
        $this->init_data($this->test_directory, $this->recursive);
    }

    public function run()
    {
        foreach ($this->test_data as $file) {
            echo $file . "\n";
        }
    }

    private function parse()
    {
        //  TODO
    }

    private function interpret()
    {
        // TODO
    }

    public function build_html()
    {
        // TODO
    }
}

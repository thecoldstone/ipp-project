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

    private $JEXAMXML_MERLIN    = '/pub/courses/ipp/jexamxml/jexamxml.jar';
    private $JEXAMCFG_MERLIN    = '/pub/courses/ipp/jexamxml/options';

    private $JEXAMXML_MAC       = '/jexamxml/jexamxml.jar';
    private $JEXAMCFG_MAC       = '/jexamxml/options';

    private $_disable_output    = true;

    private $passed             = 0;
    private $failed             = 0;

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
        if (empty($this->test_data)) {
            echo "Nothing to test...\n";
            return;
        }

        if ($this->parse_only) {

            foreach ($this->test_data as $file) {
                $this->parse($file);
            }
        } elseif ($this->int_only) {
            foreach ($this->test_data as $file) {
                $this->interpret($file);
            }
        } else {
            foreach ($this->test_data as $file) {
                $this->parse($file);
                $this->interpret($file);
            }
        }

        echo "Passed:$this->passed\nFailed:$this->failed\n";
    }

    private function parse($file)
    {
        $tmp_file = tmpfile();
        $command = "php $this->parse_script < $file";

        if ($this->_disable_output) {
            $command = $command . " 2> /dev/null";
        }

        unset($output);
        exec($command, $output, $rc);
        fwrite($tmp_file, implode("\n", $output));

        $actual_rc = file_get_contents(substr($file, 0, -3) . "rc");
        if ($actual_rc == "") {
            $actual_rc = 0;
        }

        if ($rc == $actual_rc) {
            if ($rc == 0) {
                unset($actual_xml);
                $actual_xml = substr($file, 0, -3) . "out";
                $command = "java -jar $this->jexamxml $tmp_file $actual_xml";
                exec($command, $output, $rc);

                if (preg_match("/Two files are identical/", implode("\n", $output))) {
                    $this->passed++;
                } else {
                    $this->failed++;
                }
            } else {
                $this->passed++;
            }
        } else {
            $this->failed++;
        }

        fclose($tmp_file);
    }

    private function interpret($file)
    {
        $tmp_file = tmpfile();
        $command = "python3.8 $this->int_script --source=$file";

        if ($this->_disable_output) {
            $command = $command . " 2> /dev/null";
        }

        unset($output);
        exec($command, $output, $rc);
        fwrite($tmp_file, implode("\n", $output));

        $actual_rc = file_get_contents(substr($file, 0, -3) . "rc");
        if ($actual_rc == "") {
            $actual_rc = 0;
        }

        // Do test 

        fclose($tmp_file);
    }

    public function build_html()
    {
        // TODO Can be moved to another class 
    }
}

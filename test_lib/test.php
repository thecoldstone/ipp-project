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

    private $_disable_stderr    = true;

    private $passed             = 0;
    private $failed             = 0;

    private $tmp_xml            = "tmp.xml";
    private $tmp_txt            = "tmp.txt";

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
                if ($this->parse($file))
                    $this->passed++;
                else
                    $this->failed++;
            }
        } elseif ($this->int_only) {
            foreach ($this->test_data as $file) {
                if ($this->interpret($file))
                    $this->passed++;
                else
                    $this->failed++;
            }
        } else {
            foreach ($this->test_data as $file) {
                $this->tmp_xml = substr($file, 0, -3) . "xml";
                $command = "php $this->parse_script < $file > $this->tmp_xml";
                exec($command, $output, $rc);

                if ($this->interpret($this->tmp_xml))
                    $this->passed++;
                else
                    $this->failed++;

                exec("rm $this->tmp_xml");
            }
        }

        $total_tests = count($this->test_data);
        if (file_exists($this->tmp_xml))
            exec("rm $this->tmp_xml");

        if (file_exists($this->tmp_txt))
            exec("rm $this->tmp_txt");


        if ($this->passed == 0 && $this->failed == 0 || $total_tests == 0)
            $succuess_ratio = 0;
        else
            $succuess_ratio = ($this->passed / $total_tests) * 100;

        echo "Success:$succuess_ratio\nPassed:$this->passed\nFailed:$this->failed\n-------------\nTotal:$total_tests\n";
    }

    private function parse($file)
    {
        $command = "php $this->parse_script < $file > $this->tmp_xml";

        if ($this->_disable_stderr) {
            $command = $command . " 2> /dev/null";
        }

        exec($command, $output, $rc);

        $actual_rc = file_get_contents(substr($file, 0, -3) . "rc");
        if ($actual_rc == "") {
            $actual_rc = 0;
        }

        echo "File: $file rc:$ $rc arc: $actual_rc\n";
        if ($rc == $actual_rc) {
            if ($rc == 0) {
                $actual_xml = substr($file, 0, -3) . "out";
                $command = "java -jar $this->jexamxml $this->tmp_xml $actual_xml";
                exec($command, $output, $rc);

                if (preg_match("/Two files are identical/", implode("\n", $output))) {
                    return true;
                } else {
                    return false;
                }
            } else {
                return true;
            }
        } else {
            return false;
        }
    }

    private function interpret($file)
    {
        if (file_exists(substr($file, 0, -3) . "in")) {
            $input_file = substr($file, 0, -3) . "in";
            $command = "python $this->int_script --source=$file --input=$input_file > $this->tmp_txt";
        } else {
            $command = "python $this->int_script --source=$file > $this->tmp_txt";
        }

        if ($this->_disable_stderr) {
            $command = $command . " 2> /dev/null";
        }

        exec($command, $output, $rc);

        $actual_rc = file_get_contents(substr($file, 0, -3) . "rc");
        if ($actual_rc == "") {
            $actual_rc = 0;
        }

        if ($rc == $actual_rc) {
            if ($rc == 0) {
                $actual_output = substr($file, 0, -3) . "out";
                $command = "diff $actual_output $this->tmp_txt";
                exec($command, $output, $dif_rc);
                if ($dif_rc == 0) {
                    return true;
                } else {
                    return false;
                }
            } else {
                return true;
            }
        } else {
            return false;
        }
    }

    public function build_html()
    {
        // TODO Can be moved to another class 
    }
}

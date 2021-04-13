<?php

/**
 * Project : Test Framework for IPPCode21
 * 
 * Test Framework Argument Handler Trait 
 * 
 * @author Nikita Zhukov
 * @todo Finish implementation + Implement ErrorHandler
 */

trait argumentHandler
{
    public $test_directory;
    protected $recursive;
    protected $parse_script;
    protected $int_script;
    protected $parse_only;
    protected $int_only;
    protected $jexamxml;
    protected $jexamcfg;

    /**
     * Usage method
     */
    protected function usage()
    {
        echo "Usage of test.php:\n";
        echo "\t-h, --help              Show the usage\n";
        echo "\t--directory=PATH        Test folder (if missing the current path is going to be as a test folder)\n";
        echo "\t--recursive             Test all subfolder\n";
        echo "\t--parse-script=FILE     PHP 7.4 file (program) for analyzing IPPCode21\n";
        echo "\t                        (Default file is parse.php located in the current repository)\n";

        echo "\t--int-script=FILE       Python 3.8 file (program) for interpreting XML form representation of IPPCode21\n";
        echo "\t                        (Default file is interpret.py located in the current repository)\n";

        echo "\t--parse-only            Only parsing IPPCode21\n";
        echo "\t                        (Cannot be combined with --int-only and --int-script)\n";

        echo "\t--int-only              Only interpreting XML form representation of IPPCode21\n";
        echo "\t                        (Cannot be combined with --parse-only and --parse-script)\n";

        echo "\t--jexamxml=FILE         File with JAR package with A7Soft JExamXML\n";
        echo "\t                        (Default file is /pub/courses/ipp/jexamxml/jexamxml.jar on FIT Merlin server)\n";

        echo "\t--jexamcfg=FILE         File with A7SoftJExamXML configurations\n";
        echo "\t                        (Default file is /pub/courses/ipp/jexamxml/options on FIT Merlin server)\n";
    }

    /**
     * Handler for arguments from STDIN
     */
    public function parse_args()
    {
        $optind     = 0;
        $shortopts  = "-h";
        $longopts   = array("help", "directory:", "recursive", "parse-script:", "int-script:", "parse-only", "int-only", "jexamxml:", "jexamcfg:");

        $opts = getopt($shortopts, $longopts, $optind);

        if (empty($opts)) {
            throw new Exception("The arguments are not supported");
        }

        if (array_key_exists("h", $opts) || array_key_exists("help", $opts)) {
            $this->usage();
            exit();
        }

        if (array_key_exists("directory", $opts)) {
            # Is it ok?
            if (!is_dir($opts["directory"])) {
                throw new Exception("The folder does not exist", $code = 41);
            }
            $this->test_directory = $opts["directory"];
        }

        if (array_key_exists("recursive", $opts)) {
            $this->recursive = true;
        }

        if (array_key_exists("parse-script", $opts)) {
            if (!file_exists($opts["parse-script"])) {
                throw new Exception("The file does not exist", $code = 41);
            }
            $ext = pathinfo($opts["parse-script"], PATHINFO_EXTENSION);
            if (!in_array($ext, ["php"])) {
                throw new Exception("Supported file extension for Parser is .php", $code = 41);
            }
            $this->parse_script = $opts["parse-script"];
        }

        if (array_key_exists("int-script", $opts)) {
            if (!file_exists($opts["int-script"])) {
                throw new Exception("The file does not exist", $code = 41);
            }
            $ext = pathinfo($opts["int-script"], PATHINFO_EXTENSION);
            if (!in_array($ext, ["py"])) {
                throw new Exception("Supported file extension for Interpret is .py", $code = 41);
            }
            $this->parse_script = $opts["int-script"];
        }

        if (array_key_exists("parse-only", $opts)) {
            if (array_key_exists("int-only", $opts) || array_key_exists("int-script", $opts)) {
                // throw 
            }
            $this->parse_only = true;
        }

        if (array_key_exists("int-only", $opts)) {
            if (array_key_exists("parse-only", $opts) || array_key_exists("parse-script", $opts)) {
                // throw 
            }
            $this->int_only = true;
        }

        if (array_key_exists("jexamxml", $opts)) {
            if (!file_exists($opts["jexamxml"])) {
                throw new Exception("The file does not exist", $code = 41);
            }
            $ext = pathinfo($opts["jexamxml"], PATHINFO_EXTENSION);
            if (!in_array($ext, ["jar"])) {
                throw new Exception("Supported file extension for Parser is .jar", $code = 11);
            }
            $this->parse_script = $opts["jexamxml"];
        }

        if (array_key_exists("jexamcfg", $opts)) {
            if (!file_exists($opts["jexamcfg"])) {
                throw new Exception("The file does not exist", $code = 41);
            }
            $this->parse_script = $opts["jexamcfg"];
        }
    }
}

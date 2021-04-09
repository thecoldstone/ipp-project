<?php

/**
 * Project : Parser implementation for IPPCode21
 * 
 * Class for writing to the xml file
 * 
 * @author Nikita Zhukov
 */

class DOMWriter
{

    public $dom;
    private $FILE_NAME = "output.xml";
    private $root;

    /**
     * Constructor for DOMWriter
     */
    public function __construct()
    {
        $this->dom = new DOMDocument();
        $this->dom->encoding = "UTF-8";
        $this->dom->xmlVersion = "1.0";
        $this->dom->formatOutput = true;

        $this->root();
    }

    /**
     * Initialize the root of the xml file
     */
    public function root()
    {
        $this->root = $this->dom->createElement("program");
        $rootAtt = new DOMAttr("language", "IPPcode21");
        $this->root->setAttributeNode($rootAtt);
    }

    /**
     * Set instruction and append to the xml body 
     * 
     * @param $order The number of called instruction
     * @param $opcode The current instruction
     * @param $arguments Arguments for this instruction 
     */
    public function set_instruction($order, $opcode, $arguments)
    {
        $instruction = $this->dom->createElement("instruction");
        $instructionAttOrder = new DOMAttr("order", $order);
        $instructionAttOpcode = new DOMAttr("opcode", $opcode);

        $instruction->setAttributeNode($instructionAttOrder);
        $instruction->setAttributeNode($instructionAttOpcode);

        $cnt = 0;
        foreach ($arguments as $key => $value) {
            $cnt++;
            foreach ($value as $k => $v) {
                $argument = $this->dom->createElement("arg{$cnt}", $v);
                $argument->setAttribute("type", $k);
                $instruction->appendChild($argument);
            }
        }
        $this->root->appendChild($instruction);
    }

    /**
     * Save xml file
     */
    public function save()
    {
        $this->dom->appendChild($this->root);
        $this->dom->save($this->FILE_NAME);
    }

    /**
     * Print out xml file
     */
    public function print_out()
    {
        echo $this->dom->saveXML();
    }
}

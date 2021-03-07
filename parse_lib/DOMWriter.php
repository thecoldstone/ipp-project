<?php

class DOMWriter {

    public $dom;
    private $FILE_NAME = "output.xml";
    private $root;

    public function __construct()
    {
        $this->dom = new DOMDocument();
        $this->dom->encoding = "UTF-8";
        $this->dom->xmlVersion = "1.0";

        $this->root();
    }

    public function root()
    {
        $this->root = $this->dom->createElement("program");
        $rootAtt = new DOMAttr("language", "IPPcode21");
        $this->root->setAttributeNode($rootAtt);

    }

    public function set_instruction($order, $opcode, $arguments)
    {
        $instruction = $this->dom->createElement("instruction");
        $instructionAttOrder = new DOMAttr("order", $order);
        $instructionAttOpcode = new DOMAttr("opcode", $opcode);

        $instruction->setAttributeNode($instructionAttOrder);
        $instruction->setAttributeNode($instructionAttOpcode); 
        
        $cnt = 0;
        foreach($arguments as $key => $value) {
            $cnt++;
            foreach($value as $k => $v) {
                $argument = $this->dom->createElement("arg{$cnt}", $v);
                $argument->setAttribute("type", $k);
                $instruction->appendChild($argument);
            }
        }
        $this->root->appendChild($instruction);
    }

    public function save()
    {
        $this->dom->appendChild($this->root);
        $this->dom->save($this->FILE_NAME);
    }
}
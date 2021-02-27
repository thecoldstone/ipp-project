<?php

class Stats {
    public $cntInstructions;
    public $cntComments;
    public $cntLines;

    private $flgStats; // The flag for storing stats
    private $flgLoc; // The flag for setting the counter of instructions
    private $flgComments; // The flag for setting the counter of comments
    private $flgLabel; // ???
    private $flgJumpgs;

    public $header;

    public function __construct()
    {
        $this->cntInstructions = 0;
        $this->cntComments     = 0;

        $this->header          = false;
    }

    public function addUpInstruction() {
        $this->cntInstructions += 1;
    }

    public function addUpComment() {
        $this->cntComments += 1;
    }
}
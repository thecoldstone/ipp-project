<?php

class Stats {
    protected $cntInstructions;
    protected $cntComments;
    protected $cntLines;
    protected $cntLabels;

    public function __construct()
    {
        $this->cntInstructions = 0;
        $this->cntComments     = 0;
        $this->cntLines = 0;
        $this->cntLabels = 0;
    }

    public function getInstruction() {
        return $this->cntInstructions;
    }

    public function getComment() {
        return $this->cntComments;
    }

    public function getLabel() {
        return $this->cntLabels;
    }

    public function getLine() {
        return $this->cntLines;
    }

    public function addUpInstruction() {
        $this->cntInstructions += 1;
    }

    public function addUpComment() {
        $this->cntComments += 1;
    }

    public function addUpLabel(){
        $this->cntLabels += 1;
    }

    public function addUpLine(){
        $this->cntLines += 1;
    }

    public function getStatistic(){
        return "Lines : {$this->cntLines}\n
        Instructions : {$this->cntInstructions}\n
        Comments : {$this->cntComments}\n
        Labels: {$this->cntLabels}\n";
    }
}
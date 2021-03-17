<?php
/**
 * Project : Parser implementation for IPPCode21
 * 
 * Class for storing statistics for the Parser
 * 
 * @author Nikita Zhukov
 * @todo Add the catcher for further methods (jumps, and etc. )
 */
class Stats {
    private $cntInstructions;
    private $cntComments;
    private $cntLines;
    private $cntLabels;
    private $cntJumps;

    private $curLabels;

    /**
     * Constructor for statistics
     */
    public function __construct()
    {
        $this->cntInstructions  = 0;
        $this->cntComments      = 0;
        $this->cntLines         = 0;
        $this->cntLabels        = 0;
        $this->cntJumps         = 0;

        $this->curLabels = array();
    }

    /**
     * Get the count of instructions
     * 
     * @return $this->cntInstructions
     */
    public function getInstruction() {
        return $this->cntInstructions;
    }

    /**
     * Get the count of comments
     * 
     * @return $this->cntComments
     */
    public function getComment() {
        return $this->cntComments;
    }

    /**
     * Get the count of labels
     * 
     * @return $this->cntLabels
     */
    public function getLabel() {
        return $this->cntLabels;
    }

    /**
     * Get the count of lines
     * 
     * @return $this->cntLines
     */
    public function getLine() {
        return $this->cntLines;
    }
    
    /**
     * Function for adding instruction
     */
    public function addUpInstruction() {
        $this->cntInstructions += 1;
    }

    /**
     * Function for adding comment
     */
    public function addUpComment() {
        $this->cntComments += 1;
    }

    /**
     * Function for adding label
     */
    public function addUpLabel(){
        $this->cntLabels += 1;
    }

    /**
     * Function for adding line
     */
    public function addUpLine(){
        $this->cntLines += 1;
    }

    /**
     * Function for adding jump
     */
    public function addUpJump(){
        $this->cntJumps += 1;
    }

    /**
     * Function for adding label with check whether this label has already occured
     * 
     * @param $label Label to check
     */
    public function check_label($label){
        if(!in_array($label, $this->curLabels)) {
            array_push($this->curLabels, $label);
            $this->addUpLabel();
        }
    }

    /**
     * Get current state of statistics
     */
    public function getStatistic(){
        return "Lines : {$this->cntLines}\n
        Instructions : {$this->cntInstructions}\n
        Comments : {$this->cntComments}\n
        Labels: {$this->cntLabels}\n
        Jumps: {$this->cntJumps}\n";
    }
}
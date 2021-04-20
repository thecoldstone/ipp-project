# Documentation for 2 task IPP 2020/2021

### Name and surname : Nikita Zhukov

### Login xzhuko01

Task

Implementation

## Parser

See readme1.md

## Interpreter

#### Description

Interprets XML files using stdin and stdout.

#### Interpreter library

```
- argparser.py
    * Parses arguments
- errorandler.py
    * Handles various errors and exceptions
- frames.py
    * Responsible for computation and interpretation part. Consists of Global, Local and Temporary Frames
- instructionargument.py
    * Verifies the syntax of instruction's arguments
- instruction.py
    * Verifies the syntax of instruction
- interpreter.py
    * Main file
- ippcode21.py
    * Contains all IPPCode21 instruction
- stack.py
    * Data structure for storing data. For examle, Frames, Instructions, Labels and etc.
- stats.py
    * Stores statistics during interpretation
- tockens.py
    * Represents atoms such as (Variable, Symbol)
```

## Test

#### Description

PHP script for automated testing Interpreter and Parser.

Script supports

```
-   recursive search of data for testing
-   testing of parser individually
-   testing of interpeter individually
-   combined test with parser and interpreter
```

#### Test library

```
- argumentHandler.php
    * Trait for parsing arguments
- errorHandler.php
    * Handles various errors and exceptions
- test.php
    * Main file
- testData.php
    * Trait for initializing test data
```

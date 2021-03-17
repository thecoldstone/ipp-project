# Documentation for 1 task IPP 2020/2021
### Name and surname : Nikita Zhukov
### Login xzhuko01

<p>The first part of the project covers the parsing of instruction code written in IPPCode21. The example of calling the parser is demonstrated in the parse.php</p>

### Algorithm behind the Parser.php
```
    1. Parse arguments from the terminal
    2. Init statis (logger for storing parsing statistics) according to those arguments 
    --- Main body of parser --- 
    3  Init the DOMWriter to store instructions into XML file ('output.xml')
    4. Read STDIN line by line and parse it 
    5. Save successfull instruction into xml file
```

More detailed information can be found in the coded files itself




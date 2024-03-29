import xml.etree.ElementTree as ET
import re
import sys
import os
from interpret_lib.errorhandler import (
    ExitRequest,
    InputFileError,
    IllegalXMLFormat,
    UnexpectedXMLStructure,
    SemanticError,
)
from interpret_lib.ippcode21 import IppCode21
from interpret_lib.intsruction import Instruction
from interpret_lib.stats import Stats
from interpret_lib.stack import Stack
from interpret_lib.frames import Frames


class Interpreter:
    """Main file which implements Interpreter"""

    def __init__(self, source_file, input_file=None, stats=None):
        self.source_file = source_file
        self.input_file = input_file
        if stats is None:
            self.Stats = None
        else:
            self.Stats = Stats(stats)

    @property
    def input_file(self):
        return self.__input_data

    @input_file.setter
    def input_file(self, file):
        """Downloads input data into the list

        Args:
            file (filepath): Input file with data
        """
        self.__input_data = []
        if file is None:
            self.__input_data = None
        elif os.path.isfile(file):
            with open(file) as f:
                for line in f:
                    self.__input_data.append(line.splitlines()[0])

    def input_item(self):
        """Gets input item

        Returns:
            string: Input string
        """
        if self.__input_data == []:
            return ""
        return self.__input_data.pop(0)

    def __get_xml_tree__(self):
        """Parses xml file and returns its representation as a tree

        Raises:
            InputFileError: File is damaged
            IllegalXMLFormat: XML syntax is violated

        Returns:
            tree: Element Tree instance
        """
        try:
            tree = ET.parse(self.source_file)
        except IOError:
            raise InputFileError()
        except ET.ParseError:
            raise IllegalXMLFormat()

        return tree

    def __parse_root__(self):
        """Parses root of the Element Tree

        Raises:
            UnexpectedXMLStructure: [description]
        """
        if self.root.tag != "program":
            raise UnexpectedXMLStructure(f"{self.root.tag} cannot be as a root element")

        if "language" not in self.root.attrib:
            raise UnexpectedXMLStructure('Missing attribute "language"')

        if self.root.attrib["language"].lower() != "ippcode21":
            attrib = self.root.attrib["language"]
            raise UnexpectedXMLStructure(f"Unknown language {attrib}")

        if not any(
            attrib in self.root.attrib for attrib in ["language", "name", "description"]
        ):
            raise UnexpectedXMLStructure(
                f'Not supported {list(self.root.attrib.keys())} attribute(s) for root element "program"'
            )

    def parse_xml_file(self):
        """Parses xml file and checking its syntax"""
        tree = self.__get_xml_tree__()
        self.root = tree.getroot()
        # Parse root node
        self.__parse_root__()

        self.instructions = {}
        self.labels = {}
        """Syntax analyze of XML file"""
        # Parse instructions
        for child in self.root:
            inst = Instruction()
            inst.parse(child)
            inst.parse_args(child)
            self.instructions[inst.order] = inst

            if inst.opcode == "LABEL":
                if inst.label in [v.label for k, v in self.labels.items()]:
                    raise SemanticError("Redefinition of label")
                else:
                    self.labels[inst.label] = inst

        self.instructions = sorted(
            self.instructions.items(), key=lambda index: index[0]
        )
        self.instructions = {k: v for k, v in self.instructions}

    def interpret(self):
        """Interprets XML file"""
        if not self.root:
            self.parse_xml_file()

        _CallStack = Stack()
        _DataStack = Stack()
        _Frames = Frames()

        """Interpreting code"""
        num_of_instructions = list(self.instructions.keys())
        inst_order = num_of_instructions[0]
        index = 0
        # Traversing the list of instructions which might be called using dictionary of instructions and labels
        # Index stands for instruction order
        while index < len(num_of_instructions):

            _instruction = self.instructions[num_of_instructions[index]]
            if self.Stats is not None:
                self.Stats.add_inst(_instruction)

            if _instruction.opcode == "MOVE":
                _Frames.move(_instruction.var, _instruction.symb1)
            elif _instruction.opcode == "CREATEFRAME":
                _Frames.create_frame()
            elif _instruction.opcode == "PUSHFRAME":
                _Frames.push_frame()
            elif _instruction.opcode == "POPFRAME":
                _Frames.pop_frame()
            elif _instruction.opcode == "DEFVAR":
                _Frames.defvar(_instruction.var)
            elif _instruction.opcode == "CALL":
                try:
                    _index = self.labels[_instruction.label].order
                except KeyError:
                    raise SemanticError(
                        f"Label {_instruction.label} has not been defined"
                    )
                index = num_of_instructions.index(_index)
                _CallStack.push(_instruction.order)
                continue
            elif _instruction.opcode == "RETURN":
                index = _CallStack.pop()
                continue
            elif _instruction.opcode == "PUSHS":
                _DataStack.push(_instruction.symb1)
            elif _instruction.opcode == "POPS":
                _Frames.move(_instruction.var, _DataStack.pop())
            elif _instruction.opcode == "CLEARS":
                _DataStack.clear()
            elif _instruction.opcode in ["JUMPIFEQ", "JUMPIFEQS"]:
                try:
                    _index = self.labels[_instruction.label].order
                except KeyError:
                    raise SemanticError(
                        f"Label {_instruction.label} has not been defined"
                    )

                if _instruction.opcode == "JUMPIFEQ":
                    result = _Frames.evaluate(
                        symb1=_instruction.symb1,
                        symb2=_instruction.symb2,
                        op="EQ",
                    )
                else:
                    result = _Frames.stack_ops(stack=_DataStack, op="EQS")

                if result.value is True:
                    index = num_of_instructions.index(_index)
                    continue
            elif _instruction.opcode in ["JUMPIFNEQ", "JUMPIFNEQS"]:
                try:
                    _index = self.labels[_instruction.label].order
                except KeyError:
                    raise SemanticError(
                        f"Label {_instruction.label} has not been defined"
                    )
                if _instruction.opcode == "JUMPIFNEQ":
                    result = _Frames.evaluate(
                        symb1=_instruction.symb1,
                        symb2=_instruction.symb2,
                        op="EQ",
                    )
                else:
                    result = _Frames.stack_ops(stack=_DataStack, op="EQS")
                if not result.value is True:
                    index = num_of_instructions.index(_index)
                    continue
            elif _instruction.opcode in IppCode21.stack_instructions:
                result = _Frames.stack_ops(stack=_DataStack, op=_instruction.opcode)
                _DataStack.push(result)
            elif _instruction.opcode in [
                "ADD",
                "SUB",
                "MUL",
                "IDIV",
                "LT",
                "GT",
                "EQ",
                "AND",
                "OR",
                "NOT",
                "INT2CHAR",
                "STRI2INT",
                "CONCAT",
                "STRLEN",
                "GETCHAR",
                "SETCHAR",
                "TYPE",
                "DIV",
                "INT2FLOAT",
                "FLOAT2INT",
            ]:
                _Frames.evaluate(
                    var=_instruction.var,
                    symb1=_instruction.symb1,
                    symb2=_instruction.symb2,
                    op=_instruction.opcode,
                )
            elif _instruction.opcode == "READ":
                if self.input_file is None:
                    _Frames.read(_instruction.var, _instruction.type, None)
                else:
                    _Frames.read(_instruction.var, _instruction.type, self.input_item())
            elif _instruction.opcode == "WRITE":
                _Frames.write(_instruction.symb1)
            elif _instruction.opcode == "LABEL":
                pass
            elif _instruction.opcode == "JUMP":
                try:
                    _index = self.labels[_instruction.label].order
                except KeyError:
                    raise SemanticError(
                        f"Label {_instruction.label} has not been defined"
                    )
                index = num_of_instructions.index(_index)
                continue
            elif _instruction.opcode == "EXIT":
                _Frames.exit_call(_instruction.symb1)
            elif _instruction.opcode == "DPRINT":
                # TODO
                pass
            elif _instruction.opcode == "BREAK":
                # TODO
                pass

            index += 1

        if self.Stats is not None:
            # Flash out the stats content into the file
            self.Stats.write()
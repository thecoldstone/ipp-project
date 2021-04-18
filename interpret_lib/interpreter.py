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
    def __init__(self, source_file=None, input_file=None, stats=None):
        self.source_file = source_file
        self.input_file = input_file
        self.stats = Stats(stats)

    @property
    def input_file(self):
        return self.__input_data

    @input_file.setter
    def input_file(self, file):
        self.__input_data = []
        if file is None:
            self.__input_data = None
        elif os.path.isfile(file):
            with open(file) as f:
                for line in f:
                    self.__input_data.append(line.splitlines()[0])

    def input_item(self):
        return self.__input_data.pop(0)

    def __get_xml_tree__(self):
        try:
            tree = ET.parse(self.source_file)
        except IOError:
            raise InputFileError()
        except ET.ParseError:
            raise IllegalXMLFormat()

        return tree

    def __parse_root__(self):
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
        if not self.root:
            self.parse_xml_file()

        _CallStack = Stack()
        _DataStack = Stack()
        _Frames = Frames()

        """Interpreting code"""
        num_of_instructions = list(self.instructions.keys())
        inst_order = num_of_instructions[0]
        index = 0
        while index < len(num_of_instructions):

            _instruction = self.instructions[num_of_instructions[index]]

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
            elif _instruction.opcode in ["JUMPIFEQ", "JUMPIFNEQ"]:
                # TODO
                pass
            elif _instruction.opcode == "EXIT":
                # TODO add stats
                try:
                    if (
                        int(_instruction.symb1.value) > 0
                        and int(_instruction.symb1.value) <= 49
                    ):
                        raise ExitRequest(int(_instruction.symb1.value))
                    else:
                        raise ValueError
                except ValueError:
                    raise RunTimeWrongOperandValueError
                except ExitRequest:
                    raise
            elif _instruction.opcode == "DPRINT":
                # TODO
                pass
            elif _instruction.opcode == "BREAK":
                # TODO
                pass

            index += 1

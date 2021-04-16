import xml.etree.ElementTree as ET
import re
from interpret_lib.errorhandler import (
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
                    self.labels[inst.order] = inst

    def interpret(self):
        if not self.root:
            self.parse_xml_file()

        _Stack = Stack()
        _Frames = Frames()

        """Interpreting code"""
        index = 1
        while True:

            if not self.instructions:
                break

            _instruction = self.instructions.pop(index)

            if _instruction.opcode == "MOVE":
                _Frames.move(_instruction.var, _instruction.symb1)
            elif _instruction.opcode == "CREATEFRAME":
                _Frames.create_frame()
            elif _instruction.opcode == "PUSHFRAME":
                pass
            elif _instruction.opcode == "POPFRAME":
                pass
            elif _instruction.opcode == "DEFVAR":
                _Frames.defvar(_instruction.var)
            elif _instruction.opcode == "CALL":
                pass
            elif _instruction.opcode == "RETURN":
                pass
            elif _instruction.opcode == "WRITE":
                pass
            elif _instruction.opcode == "ADD":
                _Frames.math(
                    var=_instruction.var,
                    symb1=_instruction.symb1,
                    symb2=_instruction.symb2,
                    op="ADD",
                )
            elif _instruction.opcode == "SUB":
                _Frames.math(
                    var=_instruction.var,
                    symb1=_instruction.symb1,
                    symb2=_instruction.symb2,
                    op="SUB",
                )
            elif _instruction.opcode == "MUL":
                _Frames.math(
                    var=_instruction.var,
                    symb1=_instruction.symb1,
                    symb2=_instruction.symb2,
                    op="MUL",
                )
            elif _instruction.opcode == "IDIV":
                _Frames.math(
                    var=_instruction.var,
                    symb1=_instruction.symb1,
                    symb2=_instruction.symb2,
                    op="IDIV",
                )

            index += 1
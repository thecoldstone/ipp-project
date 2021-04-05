import xml.etree.ElementTree as ET
import re
from interpret_lib.errorhandler import (
    InputFileError,
    IllegalXMLFormat,
    UnexpectedXMLStructure,
)
from interpret_lib.ippcode21 import IppCode21


class Interpreter:
    def __init__(self, source_file=None, input_file=None):
        self.source_file = source_file
        self.input_file = input_file

    def get_xml_tree(self):
        try:
            tree = ET.parse(self.source_file)
        except IOError:
            raise InputFileError()
        except ET.ParseError:
            raise IllegalXMLFormat()

        return tree

    def parse(self):
        tree = self.get_xml_tree()
        self.root = tree.getroot()
        # Parse root node
        self.parse_root()

        # Parse instructions
        self.curr_instruction = None
        self.curr_instruction_order = 0
        for child in self.root:
            self.curr_instruction_order += 1
            # Parse instruction
            self.parse_instruction(child)
            self.curr_argument_order = 0
            # Parse instruction's arguments
            for argument in child:
                self.curr_argument_order += 1
                self.parse_argument(argument)

        for child in self.root:
            pass

    def parse_root(self):
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

    def parse_instruction(self, instruction):
        if instruction.tag != "instruction":
            raise UnexpectedXMLStructure(
                f"{instruction.tag} cannot represent instruction"
            )

        if "order" not in instruction.attrib:
            raise UnexpectedXMLStructure(
                'Missing attribute "order" for instruction element'
            )

        if "opcode" not in instruction.attrib:
            raise UnexpectedXMLStructure(
                'Missing attribute "opcode" for instruction element'
            )

        try:
            order = int(instruction.attrib["order"])
            if order != self.curr_instruction_order:
                raise UnexpectedXMLStructure(
                    'Order of the instruction "{}" does not correspond to correct order'.format(
                        instruction.attrib["opcode"]
                    )
                )
        except ValueError:
            raise UnexpectedXMLStructure(
                'Order of the instruction "{}" has illegal order value {}'.format(
                    instruction.attrib["opcode"], instruction.attrib["order"]
                )
            )

        if instruction.attrib["opcode"].upper() not in IppCode21.instructions:
            raise UnexpectedXMLStructure(
                'Unknown instrucion "{}"'.format(instruction.attrib["opcode"])
            )

        self.curr_instruction = instruction.attrib["opcode"].upper()

    def parse_argument(self, argument):
        if not re.match("^arg[0-9]$", argument.tag):
            raise UnexpectedXMLStructure(
                'Unknown xml element "{}"'.format(argument.tag)
            )

        try:
            if int(argument.tag[-1]) != self.curr_argument_order:
                raise UnexpectedXMLStructure(
                    'Wrong order of argument element "{}"'.format(argument.tag)
                )
        except ValueError:
            raise UnexpectedXMLStructure(
                'Order of the argument "{}" has illegal order value {}'.format(
                    argument.tag, argument.tag[-1]
                )
            )

        if "type" not in argument.attrib:
            raise UnexpectedXMLStructure(
                'Missing attribute "type" for argument element'
            )

        if argument.attrib["type"] not in [
            "int",
            "bool",
            "string",
            "nil",
            "label",
            "type",
            "var",
        ]:
            raise UnexpectedXMLStructure(
                'Unknown "{}" type for argument element'.format(argument.attrib["type"])
            )
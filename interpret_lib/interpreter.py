import xml.etree.ElementTree as ET
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
            # Parse instruction's arguments
            for argument in child:
                self.parse_argument(argument)

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
            raise UnexpectedXMLStructure('Missing attribute "order"')

        if "opcode" not in instruction.attrib:
            raise UnexpectedXMLStructure('Missing attribute "opcode"')

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
        pass
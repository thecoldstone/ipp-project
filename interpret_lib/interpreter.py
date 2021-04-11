import xml.etree.ElementTree as ET
import re
from interpret_lib.errorhandler import (
    InputFileError,
    IllegalXMLFormat,
    UnexpectedXMLStructure,
)
from interpret_lib.ippcode21 import IppCode21
from interpret_lib.intsruction import Instruction


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

        self.instructions = []
        """Syntax analyze of XML file"""
        # Parse instructions
        for child in self.root:
            inst = Instruction()
            inst.parse(child)
            inst.parse_args(child)
            self.instructions.append(inst)

        """Interpreting code"""
        # while True:
        #     pass

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
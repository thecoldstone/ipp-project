import xml.etree.ElementTree as ET
import re
from interpret_lib.errorhandler import (
    InputFileError,
    IllegalXMLFormat,
    UnexpectedXMLStructure,
)


class Argument:
    def __init__(self, arg: ET.Element):
        self.parse(arg)

    def parse(self, arg: ET.Element):
        if not re.match("^arg[0-9]$", arg.tag):
            raise UnexpectedXMLStructure('Unknown xml element "{}"'.format(arg.tag))

        try:
            self.order = int(arg.tag[-1])
        except ValueError:
            raise UnexpectedXMLStructure(
                'Order of the argument "{}" has illegal order value {}'.format(
                    arg.tag, arg.tag[-1]
                )
            )

        if "type" not in arg.attrib:
            raise UnexpectedXMLStructure(
                'Missing attribute "type" for argument element'
            )

        if arg.attrib["type"] not in [
            "int",
            "bool",
            "string",
            "nil",
            "label",
            "type",
            "var",
        ]:
            raise UnexpectedXMLStructure(
                'Unknown "{}" type for argument element'.format(arg.attrib["type"])
            )

        self.type = arg.attrib["type"]
        self.data = arg.text
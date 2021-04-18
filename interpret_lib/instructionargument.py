import xml.etree.ElementTree as ET
import re
from interpret_lib.errorhandler import (
    InputFileError,
    IllegalXMLFormat,
    UnexpectedXMLStructure,
    RunTimeTypeError,
)


class Argument:
    def __init__(self, arg: ET.Element):
        self.parse(arg)

    def parse(self, arg: ET.Element):
        if not re.match("^arg[0-9]$", arg.tag):
            raise UnexpectedXMLStructure('Unknown xml element "{}"'.format(arg.tag))

        try:
            self.order = int(arg.tag[-1])
            if self.order < 1:
                raise UnexpectedXMLStructure(
                    'Wrong order of argument element "{}"'.format(arg.data)
                )
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

    def get_frame(self):
        pass

    def verify_var(self):
        if self.type != "var":
            raise UnexpectedXMLStructure(f"Illegal type for {self.data}")
        if self.data is None or not re.match(
            "^(GF|LF|TF)@([a-z]|[A-Z]|[\_\-\$\&\%\*\?\!])(\w|[\_\-\$\&\%\*\?\!])*$",
            self.data,
        ):
            raise UnexpectedXMLStructure(f'Illegal variable declaration "{self.data}"')

    def verify_symb(self):
        if self.type in ["int", "bool", "string", "nil", "float"]:
            if self.type == "int":
                if self.data is None or not re.match("^([+-]?[0-9]*$)", self.data):
                    raise UnexpectedXMLStructure(
                        f"Illegal variable {self.data} for int type"
                    )
            elif self.type == "bool":
                if self.data not in ["false", "true"]:
                    raise UnexpectedXMLStructure(
                        f"Illegal variable {self.data} for bool type"
                    )
            elif self.type == "string":
                if self.data is None:
                    self.data = ""
                else:
                    self.data = re.sub(
                        r"\\([0-9]{3})", lambda x: chr(int(x.group(1))), self.data
                    )
            elif self.type == "nil":
                if self.data != "nil":
                    raise UnexpectedXMLStructure(
                        f"Illegal variable {self.data} for bool type"
                    )
            elif self.type == "float":
                pass
                # TODO Finish

        elif self.type == "var":
            self.verify_var()
        else:
            raise RunTimeTypeError("Wrong symbol type")

    def verify_type(self):
        if self.type != "type":
            raise RunTimeTypeError("Wrong argument type")

    def verify_label(self):
        if self.type != "label":
            raise UnexpectedXMLStructure(f"Label type has been expected")
        if self.data is None or not re.match(
            "([a-z]|[A-Z]|[\_\-\$\&\%\*\?\!])(\w|[\_\-\$\&\%\*\?\!])*$", self.data
        ):
            raise UnexpectedXMLStructure(f"Illegal label declaration")
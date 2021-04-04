import xml.etree.ElementTree as ET
from interpret_lib.errorhandler import InputFileError, UnexpectedXMLStructure


class Interpreter:
    def __init__(self, source_file=None, input_file=None):
        self.source_file = source_file
        self.input_file = input_file

    def get_root(self):
        try:
            tree = ET.parse(self.source_file)
            root = tree.getroot()
        except IOError:
            raise InputFileError()
        except ET.ParseError:
            raise UnexpectedXMLStructure()

        return root

    def parse(self):
        root = self.get_root()
        # print(root)

        # Further parsing
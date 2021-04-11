import xml.etree.ElementTree as ET
from interpret_lib.errorhandler import (
    InputFileError,
    IllegalXMLFormat,
    UnexpectedXMLStructure,
)
from interpret_lib.ippcode21 import IppCode21
from interpret_lib.instructionargument import Argument


class Instruction(object):
    order = 1

    def __init__(self):
        self.opcode = None
        self.order = None
        self.args = None

    def parse(self, instruction: ET.Element):
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
            if int(instruction.attrib["order"]) != Instruction.order:
                raise UnexpectedXMLStructure(
                    'Wrong order of instruction "{}"'.format(
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

        self.order = Instruction.order
        self.opcode = instruction.attrib["opcode"]

        Instruction.order += 1

    def parse_args(self, instruction: ET.Element):
        self.args = []

        cur_order = 1
        for child in instruction:
            arg = Argument(child)
            if arg.order != cur_order:
                raise UnexpectedXMLStructure(
                    'Wrong order of argument element "{}"'.format(arg.data)
                )
            self.args.append(arg)
            cur_order += 1

        self.verify()

    def verify(self):
        if self.opcode in ["MOVE", "INT2CHAR", "STRLEN", "TYPE", "NOT"]:
            # OPCODE <var> <symb>
            self.verify_tockens(2)
            self.args[0].verify_var()
            self.args[1].verify_symb()
        elif self.opcode in ["CREATEFRAME", "PUSHFRAME", "POPFRAME", "RETURN", "BREAK"]:
            # OPCODE
            self.verify_tockens()
        elif self.opcode in ["DEFVAR", "POPS"]:
            # OPCODE <var>
            self.verify_tockens(1)
            self.args[0].verify_var()
        elif self.opcode in ["CALL", "LABEL", "JUMP"]:
            # OPCODE <label>
            self.verify_tockens(1)
            # self.args[0].verify_label()
        elif self.opcode in ["JUMPIFEQ", "JUMPIFNEQ"]:
            # OPCODE <label> <symb1> <symb2>
            self.verify_tockens(3)
            self.args[1].verify_symb()
            self.args[2].verify_symb()
        elif self.opcode in ["PUSHS", "WRITE", "EXIT", "DPRINT"]:
            # OPCODE <symb>
            self.verify_tockens(1)
            self.args[0].verify_symb()
        elif self.opcode in [
            "ADD",
            "SUB",
            "MULL",
            "IDIV",
            "LT",
            "GT",
            "EQ",
            "AND",
            "OR",
            "STRI2INT",
            "CONCAT",
            "GETCHAR",
            "SETCHAR",
        ]:
            # OPCODE <var> <symb1> <symb2>
            self.verify_tockens(3)
            self.args[0].verify_var()
            self.args[1].verify_symb()
            self.args[2].verify_symb()
        elif self.opcode in ["READ"]:
            # OPCODE <var> <type>
            self.verify_tockens(2)
            self.args[1].verify_var()
            self.args[2].verify_type()

    def verify_tockens(self, expected=0):
        if len(self.args) != expected:
            raise UnexpectedXMLStructure(
                'Wrong amount of arguments for instruction "{}"'.format(self.opcode)
            )

    # def __repr__(self):
    #     return f"Instruction : {self.opcode} {["arg{}" for i in self.args.keys]}"
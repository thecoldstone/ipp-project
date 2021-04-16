import xml.etree.ElementTree as ET
from interpret_lib.errorhandler import (
    InputFileError,
    IllegalXMLFormat,
    UnexpectedXMLStructure,
)
from interpret_lib.ippcode21 import IppCode21
from interpret_lib.instructionargument import Argument
from interpret_lib.tockens import Variable, Symbol


class InstructionProperties:
    def __init__(self):
        self.opcode = None
        self.order = None
        self.var = None
        self.symb1 = None
        self.symb2 = None
        self.label = None
        self.type = None


class Instruction(InstructionProperties):
    order = 1

    def __init__(self):
        super().__init__()

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
            if int(instruction.attrib["order"]) < Instruction.order:
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
        self.__args = []

        cur_order = 1
        for child in instruction:
            arg = Argument(child)
            if arg.order != cur_order:
                raise UnexpectedXMLStructure(
                    'Wrong order of argument element "{}"'.format(arg.data)
                )
            self.__args.append(arg)
            cur_order += 1

        self.verify()

    def __create_variable(self, var: str, vtype: str):
        frame, name = var.split("@")
        return Variable(name, vtype, frame)

    def __create_symbol(self, symb: str, vtype: str):
        if vtype == "var":
            return self.__create_variable(symb, vtype)
        else:
            return Symbol(symb, vtype)

    def verify(self):
        if self.opcode in ["MOVE", "INT2CHAR", "STRLEN", "TYPE", "NOT"]:
            # OPCODE <var> <symb>
            self.verify_tockens(2)
            self.__args[0].verify_var()
            self.__args[1].verify_symb()
            self.var = self.__create_variable(self.__args[0].data, self.__args[0].type)
            self.symb1 = self.__create_symbol(self.__args[1].data, self.__args[1].type)
        elif self.opcode in ["CREATEFRAME", "PUSHFRAME", "POPFRAME", "RETURN", "BREAK"]:
            # OPCODE
            self.verify_tockens()
        elif self.opcode in ["DEFVAR", "POPS"]:
            # OPCODE <var>
            self.verify_tockens(1)
            self.__args[0].verify_var()
            self.var = self.__create_variable(self.__args[0].data, self.__args[0].type)
        elif self.opcode in ["CALL", "LABEL", "JUMP"]:
            # OPCODE <label>
            self.verify_tockens(1)
            self.__args[0].verify_label()
            self.label = self.__args[0].data
        elif self.opcode in ["JUMPIFEQ", "JUMPIFNEQ"]:
            # OPCODE <label> <symb1> <symb2>
            self.verify_tockens(3)
            self.__args[0].verify_label()
            self.__args[1].verify_symb()
            self.__args[2].verify_symb()
            self.label = self.__args[0].data
            self.symb1 = self.__create_symbol(self.__args[1].data, self.__args[1].type)
            self.symb2 = self.__create_symbol(self.__args[2].data, self.__args[2].type)
        elif self.opcode in ["PUSHS", "WRITE", "EXIT", "DPRINT"]:
            # OPCODE <symb>
            self.verify_tockens(1)
            self.__args[0].verify_symb()
            self.symb1 = self.__create_symbol(self.__args[0].data, self.__args[0].type)
        elif self.opcode in [
            "ADD",
            "SUB",
            "MUL",
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
            self.__args[0].verify_var()
            self.__args[1].verify_symb()
            self.__args[2].verify_symb()
            self.var = self.__create_variable(self.__args[0].data, self.__args[0].type)
            self.symb1 = self.__create_symbol(self.__args[1].data, self.__args[1].type)
            self.symb2 = self.__create_symbol(self.__args[2].data, self.__args[2].type)
        elif self.opcode in ["READ"]:
            # OPCODE <var> <type>
            self.verify_tockens(2)
            self.__args[1].verify_var()
            self.__args[2].verify_type()
            self.var = self.__create_variable(self.__args[0].data, self.__args[0].type)
            self.type = self.__args[1].data

    def verify_tockens(self, expected=0):
        if len(self.__args) != expected:
            raise UnexpectedXMLStructure(
                'Wrong amount of arguments for instruction "{}"'.format(self.opcode)
            )
import sys
from interpret_lib.errorhandler import (
    SemanticError,
    RunTimeTypeError,
    RunTimeUndefinedVariableError,
    RunTimeUndefinedFrameError,
    RunTimeWrongOperandValueError,
    RunTimeMissingValueError,
    RunTimeIllegalStringOperationError,
    InternalError,
    ExitRequest,
)
from interpret_lib.tockens import Variable, Symbol, SYMBOL_TYPE
from interpret_lib.stack import Stack


class Frame:
    """Frame class for dealing with memory modules"""

    def __init__(self):
        self.variables = {}

    def get_var(self, var: str):
        return self.variables[var]

    def get_value(self, var: str):
        return self.variables[var].value

    def contains(self, var: Variable):
        return True if var.name in self.variables else False

    def insert(self, var: Variable):
        self.variables[var.name] = var

    def move(self, var: Variable, symb: SYMBOL_TYPE):
        self.variables[var.name].value = symb.value
        self.variables[var.name]._type = symb._type

    def copy(self, other):
        self.variables = other.variables


class GlobalFrame(Frame):
    def __init__(self):
        super().__init__()


class LocalFrame(Frame):
    def __init__(self):
        super().__init__()


class TemporaryFrame(Frame):
    def __init__(self):
        super().__init__()


class Frames:
    """Frame API enhanced by three frames such as Global Frame (GF), Local Frame (LF), Temporary Frame (TF)."""

    def __init__(self):
        self.GF = GlobalFrame()
        self.LF = None
        self.TF = None
        self.stack = Stack()

    def __get_frame(self, frame: str):
        if frame == "GF":
            return self.GF
        elif frame == "LF":
            return self.LF
        elif frame == "TF":
            return self.TF

    def __get_frame_and_var(self, var: Variable):
        """Gets frame and variable

        Args:
            var (Variable): Variable by which frame can be found

        Raises:
            RunTimeUndefinedFrameError: Frame does not exist
            RunTimeUndefinedVariableError: Variable does not exist

        Returns:
            Frame: Frame of variable
            Variable: Variable
        """
        _frame = self.__get_frame(var.frame)
        if not _frame:
            raise RunTimeUndefinedFrameError

        if not self.GF.contains(var) and not _frame.contains(var):
            raise RunTimeUndefinedVariableError(
                f'"{var.name}" does not exist in {var.frame}'
            )

        return _frame, _frame.get_var(var.name)

    def move(self, var: Variable, symb: SYMBOL_TYPE):
        """Moves symb value to var

        Args:
            var (Variable): Variable for changing
            symb (SYMBOL_TYPE): Symbol

        Raises:
            RunTimeMissingValueError: Symbol does not contain any value to move
        """
        frame, var = self.__get_frame_and_var(var)

        if type(symb) is Variable:
            _, symb = self.__get_frame_and_var(symb)

        if symb.value is None:
            raise RunTimeMissingValueError

        frame.move(var, symb)

    def create_frame(self):
        self.TF = TemporaryFrame()

    def push_frame(self):
        if not self.__get_frame("TF"):
            raise RunTimeUndefinedFrameError
        self.stack.push(self.TF)
        self.LF = LocalFrame()
        self.LF.copy(self.TF)
        self.TF = None

    def pop_frame(self):
        if not self.__get_frame("LF"):
            raise RunTimeUndefinedFrameError
        try:
            self.TF = self.stack.pop()
        except RunTimeMissingValueError:
            raise RunTimeUndefinedFrameError

    def defvar(self, var: Variable):
        _frame = self.__get_frame(var.frame)
        if not _frame:
            raise RunTimeUndefinedFrameError

        if _frame.contains(var):
            raise SemanticError("Redefinition of variable")
        else:
            _frame.insert(var)

    def evaluate(self, **kwargs):
        """Evaluation API for several IPPCode21 instructions which accepts dictionary as input parameter.

        Dictionay can contain the following attributes:
            symb1 - Symbol
            symb2 - Symbol
            var - Variable
            op - Instruction's opcode

        Returns:
            Symbol: Newly created symbol
        """
        symb1 = kwargs["symb1"]
        symb2 = kwargs["symb2"]
        frame = var = None
        if "var" in kwargs:
            frame, var = self.__get_frame_and_var(kwargs["var"])

        if type(symb1) is Variable:
            _, symb1 = self.__get_frame_and_var(symb1)

        if type(symb2) is Variable:
            _, symb2 = self.__get_frame_and_var(symb2)
        return self.__calc(
            frame=frame, var=var, symb1=symb1, symb2=symb2, op=kwargs["op"]
        )

    def stack_ops(self, **kwargs):
        """Stack evaluation API for IPPCode21 Stack Extension instructions which accepts dictionary as input parameter.

        Dictionay can contain the following attributes:
            stack - Stack with data
            op - Instruction's opcode

        Returns:
            Symbol: Newly created symbol
        """
        symb1 = symb2 = None
        if kwargs["op"] in ["NOTS", "INT2CHARS"]:
            symb1 = kwargs["stack"].item()
        else:
            symb2 = kwargs["stack"].item()
            symb1 = kwargs["stack"].item(2)

        if type(symb2) is Variable:
            _, symb2 = self.__get_frame_and_var(symb2)

        if type(symb1) is Variable:
            _, symb1 = self.__get_frame_and_var(symb1)

        return self.__calc(symb1=symb1, symb2=symb2, op=kwargs["op"][:-1])

    def __calc(self, **kwargs):
        """Main evaluation method for arithmetic, relational, boolean and formatting IPPCode21 instructions.
        Accepts dictionary as input and may contain following attributes within:
            symb1 - Symbol object or Variable object
            symb2 - Symbol object or Variable object
            var - Variable object
            stack - Stack with data
            op - Instruction's opcode

        Raises:
            RunTimeMissingValueError: Variable or Symbol does not contain any value
            RunTimeTypeError: Wrong type
            RunTimeIllegalStringOperationError: Violation of string operations
            RunTimeWrongOperandValueError: Wrong value for Variable or Symbol

        Returns:
            Symbol: Newly created symbol
        """
        frame = var = None
        result_type = "int"
        try:
            frame = kwargs["frame"]
            var = kwargs["var"]
        except KeyError:
            pass
        try:
            op = kwargs["op"]
            symb1 = kwargs["symb1"]
            symb2 = kwargs["symb2"]

            if op == "ADD":
                if symb1.value is None or symb2.value is None:
                    raise RunTimeMissingValueError
                if symb1._type != symb2._type:
                    raise RunTimeTypeError("Different types")
                if symb1._type == "int":
                    result = int(symb1.value) + int(symb2.value)
                elif symb1._type == "float":
                    result = symb1.value + symb2.value
                    result_type = "float"
                else:
                    raise RunTimeTypeError
            elif op == "SUB":
                if symb1.value is None or symb2.value is None:
                    raise RunTimeMissingValueError
                if symb1._type != symb2._type:
                    raise RunTimeTypeError("Different types")
                if symb1._type == "int":
                    result = int(symb1.value) - int(symb2.value)
                elif symb1._type == "float":
                    result = symb1.value - symb2.value
                    result_type = "float"
            elif op == "MUL":
                if symb1.value is None or symb2.value is None:
                    raise RunTimeMissingValueError
                if symb1._type != symb2._type:
                    raise RunTimeTypeError("Different types")
                if symb1._type == "int":
                    result = int(symb1.value) * int(symb2.value)
                elif symb1._type == "float":
                    result = symb1.value * symb2.value
                    result_type = "float"
            elif op == "IDIV":
                if symb1.value is None or symb2.value is None:
                    raise RunTimeMissingValueError
                if symb1._type != "int" or symb2._type != "int":
                    raise RunTimeTypeError
                result = int(int(symb1.value) / int(symb2.value))
            elif op == "DIV":
                if symb1.value is None or symb2.value is None:
                    raise RunTimeMissingValueError
                if symb1._type != symb2._type:
                    raise RunTimeTypeError("Different types")

                if symb1._type == "float":
                    result = symb1.value / symb2.value
                    result_type = "float"
                else:
                    raise RunTimeTypeError
            elif op in ["LT", "GT"]:
                if symb1.value is None or symb2.value is None:
                    raise RunTimeMissingValueError
                if symb1._type != symb2._type:
                    raise RunTimeTypeError("Different types")
                if symb1._type == "int":
                    if op == "LT":
                        result = int(symb1.value) < int(symb2.value)
                    else:
                        result = int(symb1.value) > int(symb2.value)
                elif symb1._type == "string":
                    if op == "LT":
                        result = symb1.value < symb2.value
                    else:
                        result = symb1.value > symb2.value
                elif symb1._type == "bool":
                    if op == "LT":
                        result = (
                            True
                            if symb1.value == False and symb2.value == True
                            else False
                        )
                    else:
                        result = (
                            True
                            if symb1.value == True and symb2.value == False
                            else False
                        )
                else:
                    raise RunTimeTypeError
                result_type = "bool"
            elif op == "EQ":
                if symb1.value is None or symb2.value is None:
                    raise RunTimeMissingValueError
                if symb1._type == symb2._type:
                    pass
                elif symb1._type == "nil" or symb2._type == "nil":
                    pass
                else:
                    raise RunTimeTypeError("Boolean types are expected")
                result = symb1.value == symb2.value
                result_type = "bool"
            elif op in ["AND", "OR"]:
                if symb1.value is None or symb2.value is None:
                    raise RunTimeMissingValueError
                if symb1._type != "bool" or symb2._type != "bool":
                    raise RunTimeTypeError("Boolean types are expected")
                if op == "OR":
                    result = bool(symb1.value) or bool(symb2.value)
                else:
                    result = bool(symb1.value) and bool(symb2.value)
                result_type = "bool"
            elif op == "NOT":
                if symb1.value is None:
                    raise RunTimeMissingValueError
                if symb1._type != "bool":
                    raise RunTimeTypeError("Boolean type is expected")
                result = not symb1.value
                result_type = "bool"
            elif op == "INT2CHAR":
                if symb1.value is None:
                    raise RunTimeMissingValueError
                if symb1._type != "int":
                    raise RunTimeTypeError("Integer type is expected")
                try:
                    result = chr(int(symb1.value))
                except ValueError:
                    raise RunTimeIllegalStringOperationError
                result_type = "string"
            elif op == "STRI2INT":
                if symb1.value is None or symb2.value is None:
                    raise RunTimeMissingValueError
                if symb1._type != "string" or symb2._type != "int":
                    raise RunTimeTypeError
                if int(symb2.value) < 0:
                    raise RunTimeIllegalStringOperationError

                try:
                    result = ord(symb1.value[int(symb2.value)])
                except IndexError:
                    raise RunTimeIllegalStringOperationError
            elif op == "INT2FLOAT":
                if symb1.value is None:
                    raise RunTimeMissingValueError
                if symb1._type != "int":
                    raise RunTimeTypeError
                result = float(symb1.value)
                result_type = "float"
            elif op == "FLOAT2INT":
                if symb1.value is None:
                    raise RunTimeMissingValueError
                if symb1._type != "float":
                    raise RunTimeTypeError
                result = int(symb1.value)
            elif op == "CONCAT":
                if symb1.value is None or symb2.value is None:
                    raise RunTimeMissingValueError
                if symb1._type != "string" or symb2._type != "string":
                    raise RunTimeTypeError
                result = symb1.value + symb2.value
                result_type = "string"
            elif op == "STRLEN":
                if symb1.value is None:
                    raise RunTimeMissingValueError
                if symb1._type != "string":
                    raise RunTimeTypeError
                result = len(symb1.value)
            elif op == "GETCHAR":
                if symb1.value is None or symb2.value is None:
                    raise RunTimeMissingValueError
                if symb1._type != "string" or symb2._type != "int":
                    raise RunTimeTypeError
                if int(symb2.value) < 0:
                    raise RunTimeIllegalStringOperationError
                try:
                    result = symb1.value[int(symb2.value)]
                except IndexError:
                    raise RunTimeIllegalStringOperationError
                result_type = "string"
            elif op == "SETCHAR":
                if var.value is None:
                    raise RunTimeMissingValueError
                if symb1.value is None or symb2.value is None:
                    raise RunTimeMissingValueError

                if var._type != "string":
                    raise RunTimeTypeError
                if symb1._type != "int" or symb2._type != "string":
                    raise RunTimeTypeError
                if int(symb1.value) < 0:
                    raise RunTimeIllegalStringOperationError

                if len(symb2.value) == 0:
                    raise RunTimeIllegalStringOperationError
                try:
                    result = list(var.value)
                    result[int(symb1.value)] = str(symb2.value[0])
                    result = "".join(result)
                except IndexError:
                    raise RunTimeIllegalStringOperationError
                result_type = "string"
            elif op == "TYPE":
                if symb1._type == "var":
                    result = ""
                    result_type = "string"
                else:
                    result = symb1._type
                    result_type = "string"
        except ValueError:
            raise RunTimeTypeError
        except ZeroDivisionError:
            raise RunTimeWrongOperandValueError("Division by zero")

        if frame and var:
            frame.move(var, Symbol(result, result_type))
        else:
            return Symbol(result, result_type)

    def read(self, var: Variable, vtype: str, content):
        """Implementation of Read instruction. Moves content to var

        Args:
            var (Variable): Variable to change
            vtype (str): Type of data to read
            content ([string]): Content to insert

        Raises:
            ValueError: [description]
        """
        _frame, _var = self.__get_frame_and_var(var)

        try:
            if content is None:
                content = input()

            if vtype == "int":
                content = int(content)
            elif vtype == "float":
                content = float(content)
            elif vtype == "string":
                content = str(content)
            elif vtype == "bool":
                if content.lower() == "true":
                    content = True
                elif content.lower() == "false":
                    content = False
                else:
                    raise ValueError
        except ValueError:
            if vtype == "float":
                try:
                    content = float.fromhex(content)
                except Exception:
                    content = "nil"
                    vtype = "nil"
            else:
                content = "nil"
                vtype = "nil"
        finally:
            _frame.move(_var, Symbol(content, vtype))

    def write(self, symb: SYMBOL_TYPE):
        """Implementation of Write instruction. Prints out to STDOUT value of symb

        Args:
            symb (SYMBOL_TYPE): Variable or Symbol

        Raises:
            RunTimeMissingValueError: [description]
        """
        if type(symb) is Variable:
            frame, var = self.__get_frame_and_var(symb)
        else:
            var = symb

        if var.value is None:
            raise RunTimeMissingValueError

        out_string = ""

        if var._type == "bool":
            out_string = "true" if var.value is True else "false"
        elif var._type == "nil":
            out_string = ""
        elif var._type == "float":
            out_string = float.hex(var.value)
        else:
            out_string = var.value

        print(out_string, end="")

    def exit_call(self, symb: SYMBOL_TYPE):
        """Implementation of Exit instruction.

        Args:
            symb (SYMBOL_TYPE): Variable or Symbol which contains integer value

        Raises:
            RunTimeMissingValueError: Element does not contain any value
            RunTimeTypeError: Element has wrong type. Integer is expected
            ExitRequest: Raises exit request to finish program as User has asked
            RunTimeWrongOperandValueError: Exit code is reserved
        """
        if type(symb) is Variable:
            frame, var = self.__get_frame_and_var(symb)
        else:
            var = symb

        if var.value is None:
            raise RunTimeMissingValueError
        elif var._type != "int":
            raise RunTimeTypeError
        else:
            if int(var.value) > 0 and int(var.value) <= 49:
                raise ExitRequest(int(var.value))
            else:
                raise RunTimeWrongOperandValueError

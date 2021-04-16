from typing import Union
from interpret_lib.errorhandler import (
    SemanticError,
    RunTimeTypeError,
    RunTimeUndefinedVariableError,
    RunTimeUndefinedFrameError,
    RunTimeWrongOperandValueError,
    InternalError,
)
from interpret_lib.tockens import Variable, Symbol

SYMBOL_TYPE = Union[Symbol, Variable]
VARIABLE_TYPE = Union[int, str, bool, None]


class Frame:
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

    def move(self, var: Variable, value):
        self.variables[var.name].value = value


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
    def __init__(self):
        self.GF = GlobalFrame()
        self.LF = None
        self.TF = None

    def __get_frame(self, frame: str):
        if frame == "GF":
            return self.GF
        elif frame == "LF":
            return self.LF
        elif frame == "TF":
            return self.TF

    def __get_frame_and_var(self, var: Variable):
        _frame = self.__get_frame(var.frame)
        if not _frame:
            raise RunTimeUndefinedFrameError

        if not self.GF.contains(var) and not _frame.contains(var):
            raise RunTimeUndefinedVariableError(
                f'"{var.name}" does not exist in {var.frame}'
            )

        return _frame, _frame.get_var(var.name)

    def has_variable(self, var: Variable):
        _frame = self.__get_frame(var.frame)
        if not _frame:
            raise RunTimeUndefinedFrameError
        # TODO

    def create_frame(self):
        pass
        # TODO

    def defvar(self, var: Variable):
        _frame = self.__get_frame(var.frame)
        if not _frame:
            raise RunTimeUndefinedFrameError

        if self.GF.contains(var) or _frame.contains(var):
            raise SemanticError("Redefinition of variable")
        else:
            _frame.insert(var)

    def move(self, var: Variable, symb: SYMBOL_TYPE):
        _frame, _var = self.__get_frame_and_var(var)

        if type(symb) is Variable:
            _ = self.__var_exists(symb)

        _frame.move(_var, symb.value)

    def __set_symb(self, symb: SYMBOL_TYPE, operation: str):
        _symb = symb
        if type(symb) is Variable:
            _frame = self.__get_frame(symb.frame)
            _symb = _frame.get_var(symb.name)
            if _symb._type == "var":
                if operation == "math":
                    _symb.value = 0
                    _frame.variables[symb.name]._type = "int"

        return _symb

    def math(self, **kwargs):
        if "var" in kwargs:
            _frame, _var = self.__get_frame_and_var(kwargs["var"])
        if "symb1" in kwargs:
            symb1 = self.__set_symb(kwargs["symb1"], "math")
        if "symb2" in kwargs:
            symb2 = self.__set_symb(kwargs["symb2"], "math")
        if "op" in kwargs:
            self.__calc(_frame, _var, symb1, symb2, kwargs["op"])

    def __calc(
        self,
        frame: Frame,
        var: Variable,
        symb1: SYMBOL_TYPE,
        symb2: SYMBOL_TYPE,
        op: str,
    ):
        try:
            if op == "ADD":
                frame.move(var, int(symb1.value) + int(symb2.value))
            elif op == "SUB":
                frame.move(var, int(symb1.value) - int(symb2.value))
            elif op == "MUL":
                frame.move(var, int(symb1.value) * int(symb2.value))
            elif op == "IDIV":
                try:
                    frame.move(var, int(int(symb1.value) / int(symb2.value)))
                except ZeroDivisionError:
                    raise RunTimeWrongOperandValueError("Division by zero")
        except TypeError as e:
            raise

        print(frame.variables[var.name].value)
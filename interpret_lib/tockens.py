from typing import Union


class Tocken:
    def __init__(self, name=None, value=None, _type=None):
        self.name = name
        self.value = value
        self._type = _type

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):
        self.__name = name

    @property
    def _type(self):
        return self.__type

    @_type.setter
    def _type(self, _type: str):
        self.__type = _type


class Variable(Tocken):
    def __init__(self, name: str, vtype: str, frame=None, value=None):
        super().__init__(name, value, vtype)
        self.frame = frame


class Symbol(Tocken):
    def __init__(self, value: str, stype):
        super().__init__(value=value, _type=stype)


SYMBOL_TYPE = Union[Symbol, Variable]
VARIABLE_TYPE = Union[int, str, bool, None]
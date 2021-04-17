from interpret_lib.errorhandler import RunTimeMissingValueError, InternalError
from interpret_lib.tockens import Symbol, Variable, SYMBOL_TYPE


class Stack:
    def __init__(self):
        self.stack = []

    def is_empty(self):
        return self.stack == []

    def push(self, data):
        self.stack.append(data)

    def pop(self):
        if self.is_empty():
            raise RunTimeMissingValueError("Stack is empty")
        else:
            return self.stack.pop()

    def top(self):
        if self.is_empty():
            raise RunTimeMissingValueError("Stack is empty")
        else:
            return self.stack[-1]

    def item(self, i=1):
        try:
            return self.stack[-i]
        except Exception:
            raise InternalError("Stack overflow")

    def clear(self):
        self.stack = []

from interpret_lib.errorhandler import RunTimeMissingValueError


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

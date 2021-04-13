# from interpret_lib.errorhandler import ()


class Frame:
    def __init__(self):
        self.variables = {}


class GlobalFrame(Frame):
    def __init__(self):
        super().__init__()


class LocalFrame(Frame):
    def __init__(self):
        super().__init__()


class TemporaryFrame(Frame):
    def __init__(self):
        super().__init__()
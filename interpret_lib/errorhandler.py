class ExceptionBase(Exception):
    # TODO Finish msg texts for errors
    def __init__(self, exit_status: int, msg=None):
        if exit_status == 10:
            self.msg = "Missing argument or invalid argument"
        elif exit_status == 11:
            self.msg = "File cannot be opened because it might not exist or you don't have permission"
        elif exit_status == 31:
            self.msg = "Illegal xml format"
        elif exit_status == 32:
            self.msg = "Unexpected xml structure"
        elif exit_status == 52:
            self.msg = "Semantic error"
        elif exit_status == 53:
            self.msg = "Illegal type of operand"
        elif exit_status == 54:
            self.msg = "Undefined variable"
        elif exit_status == 55:
            self.msg = "Frame does not exist"
        elif exit_status == 56:
            self.msg = "Missing value"
        elif exit_status == 57:
            self.msg = "Value error"
        elif exit_status == 58:
            self.msg = "Illegal operations with string literal"
        elif exit_status == 99:
            self.msg = "Internal error"

        if msg is not None:
            self.msg += f"\nDetailed info: {msg}\n"

        self.exit_status = exit_status


class MissingArgError(ExceptionBase):
    def __init__(self, msg=None):
        self.exit_status = 10
        super().__init__(self.exit_status, msg)


class InputFileError(ExceptionBase):
    def __init__(self, msg=None):
        self.exit_status = 11
        super().__init__(self.exit_status, msg)


class IllegalXMLFormat(ExceptionBase):
    def __init__(self, msg=None):
        self.exit_status = 31
        super().__init__(self.exit_status, msg)


class UnexpectedXMLStructure(ExceptionBase):
    def __init__(self, msg=None):
        self.exit_status = 32
        super().__init__(self.exit_status, msg)


class SemanticError(ExceptionBase):
    def __init__(self, msg=None):
        self.exit_status = 52
        super().__init__(self.exit_status, msg)


class RunTimeTypeError(ExceptionBase):
    def __init__(self, msg=None):
        self.exit_status = 53
        super().__init__(self.exit_status, msg)


class RunTimeUndefinedVariableError(ExceptionBase):
    def __init__(self, msg=None):
        self.exit_status = 54
        super().__init__(self.exit_status, msg)


class RunTimeUndefinedFrameError(ExceptionBase):
    def __init__(self, msg=None):
        self.exit_status = 55
        super().__init__(self.exit_status, msg)


class RunTimeMissingValueError(ExceptionBase):
    def __init__(self, msg=None):
        self.exit_status = 56
        super().__init__(self.exit_status, msg)


class RunTimeWrongOperandValueError(ExceptionBase):
    def __init__(self, msg=None):
        self.exit_status = 57
        super().__init__(self.exit_status, msg)


class RunTimeIllegalStringOperationError(ExceptionBase):
    def __init__(self, msg=None):
        self.exit_status = 58
        super().__init__(self.exit_status, msg)


class InternalError(ExceptionBase):
    def __init__(self, msg=None):
        self.exit_status = 99
        super().__init__(self.exit_status, msg)
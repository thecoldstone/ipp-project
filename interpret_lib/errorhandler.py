class ExceptionBase(Exception):
    def __init__(self, msg, exit_status: int):
        if msg is None:
            if exit_status == 10:
                self.msg = "Missing argument or invalid argument"
            elif exit_status == 11:
                self.msg = "File cannot be opened because it might not exist or you don't have permission"
            elif exit_status == 32:
                self.msg = "Unexpected xml structure"
            elif exit_status == 99:
                self.msg = "Internal error"

        self.exit_status = exit_status


class MissingArgError(ExceptionBase):
    def __init__(self, msg=None):
        self.exit_status = 10
        super().__init__(msg, self.exit_status)


class InputFileError(ExceptionBase):
    def __init__(self, msg=None):
        self.exit_status = 11
        super().__init__(msg, self.exit_status)


class UnexpectedXMLStructure(ExceptionBase):
    def __init__(self, msg=None):
        self.exit_status = 32
        super().__init__(msg, self.exit_status)


class InternalError(ExceptionBase):
    def __init__(self, msg=None):
        self.exit_status = 99
        super().__init__(msg, self.exit_status)
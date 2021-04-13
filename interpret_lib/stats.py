# TODO Finish
class Stats:
    def __init__(self, kwargs: dict):
        self.file = None
        self.insts = None
        self.hot = None
        self.vars = None

        if kwargs["file"]:
            self.file = kwargs["file"]

        if kwargs["insts"]:
            self.insts = 0

        if kwargs["hot"]:
            self.hot = 0

        if kwargs["vars"]:
            self.vars = 0

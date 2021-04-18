from interpret_lib.ippcode21 import IppCode21
from interpret_lib.intsruction import Instruction


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
            self.hot = {}

        if kwargs["vars"]:
            self.vars = 0

    def add_inst(self, inst: Instruction):
        if self.insts is None:
            return
        if (
            inst.opcode not in IppCode21.instructions
            and inst.opcode not in IppCode21.stack_instructions
        ):
            return
        if inst.opcode in ["LABEL", "DPRINT", "BREAK"]:
            return

        if self.hot is not None:
            if inst.order in self.hot:
                self.hot[inst.order] += 1
            else:
                self.hot[inst.order] = 0
        self.insts += 1

    def get_hot(self):
        return sorted(self.hot.items(), key=lambda index: (-index[1], index[0]))[0][0]

    def add_var(self):
        # TODO
        pass

    def write(self):
        with open(self.file, "w") as f:
            if self.insts is not None:
                f.write(f"{str(self.insts)}\n")
            if self.hot is not None:
                f.write(f"{str(self.get_hot())}\n")

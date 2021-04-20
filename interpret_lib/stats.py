from interpret_lib.ippcode21 import IppCode21
from interpret_lib.intsruction import Instruction


class Stats:
    """Stats class representing statistics of Interperter

    Attributes:
    ----------
        file: filpath
            File to store statistics
        insts: int
            Counter of called instructions
        hot: dict
            Dictionary of most used instructions
        vars:
            Counter of initialized variables
    """

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
        """Adds instruction

        Args:
            inst (Instruction): Some object of Instruction class with defined attributes
        """
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
        """Gets the most used instruction in program

        Returns:
           int : number of most called instruction
        """
        return sorted(self.hot.items(), key=lambda index: (-index[1], index[0]))[0][0]

    def add_var(self):
        """Adds variables"""
        # TODO
        pass

    def write(self):
        """Writes to file"""
        with open(self.file, "w") as f:
            if self.insts is not None:
                f.write(f"{str(self.insts)}\n")
            if self.hot is not None:
                f.write(f"{str(self.get_hot())}\n")

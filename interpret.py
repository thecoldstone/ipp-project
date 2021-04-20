import os
import sys
from interpret_lib.argsparser import args_parser
from interpret_lib.interpreter import Interpreter
from interpret_lib.errorhandler import ExitRequest

if __name__ == "__main__":

    exit_status = 0
    try:
        source_file, input_file, stats = args_parser()

        if not source_file:
            source_file = "tmp.xml"
            with open(source_file, "w") as tmp:
                for line in sys.stdin:
                    tmp.write(line)

        interpreter = Interpreter(source_file, input_file, stats)
        interpreter.parse_xml_file()
        interpreter.interpret()
    except ExitRequest as e:
        exit_status = e.exit_status
    except Exception as e:
        if hasattr(e, "msg"):
            if e.exit_status > 52:
                print(f"[RUNTIME ERROR] {e.msg}")
            else:
                print(f"[ERROR] {e.msg}")
        else:
            raise
            # print(f"[INTERNAL ERROR] {e}")

        if hasattr(e, "exit_status"):
            exit_status = e.exit_status

    if os.path.exists("tmp.xml"):
        os.remove("tmp.xml")

    sys.exit(exit_status)

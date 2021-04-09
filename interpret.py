from interpret_lib.argsparser import args_parser
from interpret_lib.interpreter import Interpreter

if __name__ == "__main__":

    try:
        args = args_parser()
        interpreter = Interpreter(args[0], args[1])
        interpreter.parse()

    except Exception as e:
        if hasattr(e, "msg"):
            print(f"[ERROR] {e.msg}")
        else:
            # print(f"[INTERNAL ERROR] {e}")
            raise

        if hasattr(e, "exit_status"):
            exit(e.exit_status)
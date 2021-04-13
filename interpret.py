from interpret_lib.argsparser import args_parser
from interpret_lib.interpreter import Interpreter

if __name__ == "__main__":

    try:
        source_file, input_file, stats = args_parser()
        interpreter = Interpreter(source_file, input_file, stats)
        interpreter.parse_xml_file()
        interpreter.interpret()

    except Exception as e:
        if hasattr(e, "msg"):
            if e.exit_status > 52:
                print(f"[RUNTIME ERROR] {e.msg}")
            else:
                print(f"[ERROR] {e.msg}")
        else:
            # print(f"[INTERNAL ERROR] {e}")
            raise

        if hasattr(e, "exit_status"):
            exit(e.exit_status)
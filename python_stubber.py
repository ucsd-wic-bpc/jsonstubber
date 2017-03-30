from .json_stubber import (
    JSONStubber, StubSection, TextStubSection, JSONTypes, JSONContainer
)


class PythonJSONStubber(JSONStubber):

    def __init__(self,
                 jsonfastparse_path='jsonfastparse',
                 unifiedstr_path='unifiedstr'):

        self.jsonfastparse_path = jsonfastparse_path
        self.unifiedstr_path = unifiedstr_path

    def make_file_without_body(self, class_name):
        import_lines, body_lines = self.make_jsonparsing_lines()
        return StubSection(header="\n".join(import_lines), footer="\n".join(body_lines), tabs=-1)

    def make_jsonparsing_lines(self):
        import_lines = [
            "import json",
            "import sys"
        ]

        body_lines = [
            "if __name__ == '__main__':",
            "    sys.exit(main())"
        ]

        return import_lines, body_lines

    def get_default_return(self, stubtype):
        if isinstance(stubtype, JSONContainer):
            return "[]"
        elif stubtype == JSONTypes.INT:
            return "0"
        elif stubtype == JSONTypes.FLOAT:
            return "0.0"
        elif stubtype == JSONTypes.STRING:
            return '""'
        elif stubtype == JSONTypes.CHAR:
            return "''"
        elif stubtype == JSONTypes.BOOL:
            return "False"

    def make_userimpl_section(self, method_name, return_type, arguments):
        argument_names = [argument_name for (argument_name, argtype) in arguments]
        header = "def {}({}):".format(method_name, ", ".join(argument_names))
        body_lines = ["# TODO"]
        body_lines.append("return {}".format(self.get_default_return(return_type)))

        body_section = TextStubSection("\n".join(body_lines))

        return StubSection(header=header, child_sections=[body_section], footer="")

    def make_main_without_body(self):
        header = "def main():"

        return StubSection(header=header, footer="")

    def make_parse_input(self):
        parse_lines = [
            "arg_list = json.loads(raw_input())",
        ]

        return TextStubSection("\n".join(parse_lines))

    def make_arg_process(self, argnum, argument_name, argument_type):
        return TextStubSection("{} = arg_list[{}]".format(argument_name, argnum))

    def make_process_output(self, return_type, method_name, arguments):
        argnames = [argname for (argname, argtype) in arguments]
        output_str = "output = {}({})".format(method_name, ", ".join(argnames))
        print_str = "print(output)"

        return TextStubSection("{}\n{}".format(output_str, print_str))

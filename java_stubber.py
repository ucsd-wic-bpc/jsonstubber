from .json_stubber import JSONStubber, StubSection, TextStubSection
from .pyjsontypes.jsontypes import JSONTypes, JSONContainer
import glob
import os

class JavaJSONStubber(JSONStubber):

    def __init__(self,
                 jsonfastparse_path='jsonfastparse',
                 unifiedstr_path='unifiedstr'):

        self.jsonfastparse_path = jsonfastparse_path
        self.unifiedstr_path = unifiedstr_path

    def make_file_without_body(self, class_name):
        import_lines, support = self.make_supportfile_lines()
        class_line = "public class {} {{".format(class_name)
        end_class_line = "}"
        header = "{}\n{}\n".format("".join(import_lines), class_line)
        footer = "{}\n{}".format(end_class_line, "".join(support))

        return StubSection(header=header, footer=footer)

    def make_supportfile_lines(self):
        # First, let's gather the chunk of text from JSONFastParse
        import_lines = []
        lines = []
        files = glob.glob(os.path.join(self.jsonfastparse_path, 'Java/*.java'))
        files += glob.glob(os.path.join(self.unifiedstr_path, "Java/*.java"))
        for support_file in files:
            with open(support_file, 'r') as f:
                line = f.readline()
                while line:
                    if line.startswith("import "):
                        import_lines.append(line)
                    else:
                        lines.append(line)
                    line = f.readline()

        import_lines += [
            "import java.util.Scanner;\n",
        ]

        return import_lines, lines

    def get_default_return(self, stubtype):
        if isinstance(stubtype, JSONContainer):
            return "new {}{{}}".format(self.convert_to_language_type(stubtype))
        else:
            if stubtype == JSONTypes.INT: return "0"
            if stubtype == JSONTypes.FLOAT: return "0.0"
            if stubtype == JSONTypes.STRING: return '""'
            if stubtype == JSONTypes.CHAR: return "'\0'"


    def convert_to_language_type(self, stubtype):
        if isinstance(stubtype, JSONContainer):
            return "{}[]".format(self.convert_to_language_type(stubtype.subtype))
        else:
            if stubtype == JSONTypes.INT: return "int"
            if stubtype == JSONTypes.FLOAT: return "double"
            if stubtype == JSONTypes.STRING: return "String"
            if stubtype == JSONTypes.CHAR: return "char"

    def make_userimpl_section(self, method_name, return_type, arguments):
        lang_ret_type = self.convert_to_language_type(return_type)
        arglist = [(name, self.convert_to_language_type(argtype)) for (name, argtype) in arguments]
        arglist = ", ".join(["{} {}".format(langtype, name) for (name, langtype) in arglist])
        header = "public static {} {}({}) {{".format(lang_ret_type, method_name, arglist)
        body_lines = [
            "//TODO",
            "return {};".format(self.get_default_return(return_type))
        ]
        body = TextStubSection("\n".join(body_lines))
        footer = "}\n"

        return StubSection(header=header, child_sections=[body], footer=footer, tabs=0)

    def make_main_without_body(self):
        header = "public static void main(String[] args) {"
        footer = "}"

        return StubSection(header=header, footer=footer)

    def make_parse_input(self):
        lines = ["String input = new Scanner(System.in).nextLine();",
                 "JSONList argList = (JSONList) JSONParser.getObjectFromString(input);"
                ]
        return TextStubSection("\n".join(lines))

    def get_container_base_type(self, arrtype):
        while isinstance(arrtype, JSONContainer):
            arrtype = arrtype.subtype
        
        return self.convert_to_language_type(arrtype)

    def make_array(self, argnum, argument_name, arrtype):
        lines = self.make_array_wrapper(argnum, "argList", argument_name, arrtype)
        return TextStubSection("\n".join(lines))

    def make_array_wrapper(self, argnum, base_list, argument_name, arrtype, tab_count=0):
        lang_type = self.convert_to_language_type(arrtype)
        tabs = "\t" * tab_count
        if not isinstance(arrtype, JSONContainer):
            return "{}.getItem({}).castTo{}()".format(base_list, argnum, lang_type.title())

        jsonlist_name = "{}jsonlist".format(argument_name)
        it_index = "i{}".format(arrtype.degree)
        lines = [
            "{}JSONList {} = (JSONList) {}.getItem({});".format(tabs, jsonlist_name, base_list, argnum),
            "{}{} {} = {};".format(tabs,lang_type, argument_name, 
                                self.make_new_array_str(arrtype, "{}.getEntryCount()".format(jsonlist_name))),
            "{0}for (int {1} = 0; {1} < {2}.length; {1}++) {{".format(tabs, it_index, argument_name)
        ]

        subtype = arrtype.subtype
        if not isinstance(subtype, JSONContainer):
            lang_subtype = self.convert_to_language_type(subtype).title()
            assign_str = "{}.getItem({}).castTo{}()".format(jsonlist_name, it_index, lang_subtype)
        else:
            new_argname = "{}{}".format(argument_name, arrtype.degree)
            lines += self.make_array_wrapper(it_index, jsonlist_name, new_argname, subtype, tab_count=tab_count+1)
            assign_str = new_argname

        lines += [
            "{}{}[{}] = {};".format(tabs + "\t", argument_name, it_index, assign_str),
            "{}}}".format(tabs)
        ]

        return lines

    def make_new_array_str(self, arrtype, size_str):
        base_type = self.get_container_base_type(arrtype)
        degree_less_one = int(arrtype.degree) - 1
        return "new {}[{}]".format(base_type, size_str) + ("[]" * degree_less_one)

    def make_arg_process(self, argnum, argument_name, argument_type):
        if not isinstance(argument_type, JSONContainer):
            lang_type = self.convert_to_language_type(argument_type)
            return TextStubSection(
                    "{} {} = argList.getItem({}).castTo{}();".format(
                    lang_type, argument_name, argnum, lang_type.title())
                   )
        else:
            return self.make_array(argnum, argument_name, argument_type)

    def make_process_output(self, return_type, method_name, arguments):
        lang_ret_type = self.convert_to_language_type(return_type)
        argument_names = [argname for (argname, argtype) in arguments]
        lines = [
            "{} output = {}({});".format(lang_ret_type, method_name, ", ".join(argument_names))
        ]

        if isinstance(return_type, JSONContainer):
            lines.append("System.out.println(Unifiedstr.deepToString(output));");
        else:
            lines.append("System.out.println(Unifiedstr.toString(output));");

        return TextStubSection("\n".join(lines))

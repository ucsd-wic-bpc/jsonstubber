from json_stubber import JSONStubber, StubSection, TextStubSection, JSONTypes, JSONType, JSONContainer
import glob

class JavaJSONStubber(JSONStubber):

    def make_file_without_body(self, class_name):
        import_lines, jsonfast = self.make_jsonfastparse_lines()
        class_line = "public class {} {{".format(class_name)
        end_class_line = "}"
        header = "{}\n{}".format("".join(import_lines), class_line)
        footer = "{}\n{}".format(end_class_line, "".join(jsonfast))

        return StubSection(header=header, footer=footer)

    def make_jsonfastparse_lines(self):
        # First, let's gather the chunk of text from JSONFastParse
        import_lines = []
        lines = []
        files = glob.glob("jsonfastparse/Java/*.java")
        for jsonfastparse_file in files:
            with open(jsonfastparse_file, 'r') as f:
                line = f.readline()
                while line:
                    if line.startswith("import "):
                        import_lines.append(line)
                    else:
                        lines.append(line)
                    line = f.readline()

        import_lines.append("import java.util.Scanner;")
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
        footer = "}"

        return StubSection(header=header, child_sections=[body], footer=footer)

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

    def make_array_wrapper(self, argnum, base_list, argument_name, arrtype):
        lang_type = self.convert_to_language_type(arrtype)
        if not isinstance(arrtype, JSONContainer):
            return "{}.getItem({}).castTo{}()".format(base_list, argnum, lang_type.title())

        jsonlist_name = "{}jsonlist".format(argument_name)
        it_index = "i{}".format(arrtype.degree)
        lines = [
            "JSONList {} = (JSONList) {}.getItem({});".format(jsonlist_name, base_list, argnum),
            "{} {} = {};".format(lang_type, argument_name, 
                                self.make_new_array_str(arrtype, "{}.getEntryCount()".format(jsonlist_name))),
            "for (int {0} = 0; {0} < {1}.length; {0}++) {{".format(it_index, argument_name)
        ]

        subtype = arrtype.subtype
        if not isinstance(subtype, JSONContainer):
            lang_subtype = self.convert_to_language_type(subtype).title()
            assign_str = "{}.getItem({}).castTo{}()".format(jsonlist_name, it_index, lang_subtype)
        else:
            new_argname = "{}{}".format(argument_name, arrtype.degree)
            lines += self.make_array_wrapper(it_index, jsonlist_name, new_argname, subtype)
            assign_str = new_argname

        lines += [
            "{}[{}] = {};".format(argument_name, it_index, assign_str),
            "}"
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

    def get_convert_output_to_string(self, return_type):
        if return_type == JSONTypes.BOOL:
            return 'String output_str = output ? "True" : "False";'
        else:
            return "String output_str = output;"

    def make_process_output(self, return_type, method_name, arguments):
        lang_ret_type = self.convert_to_language_type(return_type)
        lines = [
            "{} output = {}({});".format(lang_ret_type, method_name, ", ".join(arguments))
        ]

        lines.append(self.get_convert_output_to_string(return_type))
        lines.append("System.out.println(output_str);");

        return TextStubSection("\n".join(lines))

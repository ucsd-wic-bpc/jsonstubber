from json_stubber import (
    JSONStubber, StubSection, TextStubSection, JSONTypes, JSONContainer
)
import glob
import os


class CppJSONStubber(JSONStubber):

    def __init__(self,
                 jsonfastparse_path='jsonfastparse',
                 unifiedstr_path='unifiedstr'):

        self.jsonfastparse_path = jsonfastparse_path
        self.unifiedstr_path = unifiedstr_path

    def make_file_without_body(self, class_name):
        include_lines, header_lines, body_lines = self.make_supportfile_lines()
        self.header_lines = header_lines
        header = "".join(include_lines)
        footer = "".join(body_lines)

        return StubSection(header=header, footer=footer)

    def get_hpp_header_lines(self, hpp_file, finished_deps=None):
        hpp_base_dir = os.path.dirname(hpp_file)
        finished_deps = finished_deps or []
        header_lines = []
        include_lines = set()

        if hpp_file in finished_deps:
            return set(), [], []

        finished_deps.append(hpp_file)

        with open(hpp_file, 'r') as f:
            line = f.readline()
            while line:
                if line.startswith('#include "'):
                    depend_header_file = line[len('#include "'):].strip()[:-1]
                    depend_header_file = os.path.join(hpp_base_dir, depend_header_file)
                    includes, heads, deps = self.get_hpp_header_lines(depend_header_file, finished_deps)
                    header_lines = heads + header_lines
                    include_lines |= includes
                    finished_deps.extend(deps)
                elif line.startswith('#include <'):
                    include_lines.add(line)
                else:
                    header_lines.append(line)

                line = f.readline()

        return include_lines, header_lines, finished_deps

    def make_supportfile_lines(self):
        # First, let's gather the chunk of text from JSONFastParse
        include_lines = set()
        header_lines = []
        finished_header_files = []
        header_files = glob.glob(os.path.join(self.jsonfastparse_path, "C++", "*.hpp"))
        header_files += glob.glob(os.path.join(self.unifiedstr_path, "C++", "*.hpp"))
        for jsonfast_header in header_files:
            if jsonfast_header in finished_header_files:
                continue

            includes, lines, files = self.get_hpp_header_lines(jsonfast_header, finished_deps=finished_header_files)
            include_lines |= includes
            header_lines.extend(lines)
            finished_header_files.extend(files)

        body_lines = []
        body_files = glob.glob(os.path.join(self.jsonfastparse_path, "C++", "*.cpp"))
        body_files += glob.glob(os.path.join(self.unifiedstr_path, "C++", "*.cpp"))
        for jsonfast_body in body_files:
            with open(jsonfast_body, 'r') as f:
                line = f.readline()
                while line:
                    if line.startswith("#include <"):
                        include_lines.add(line)
                    elif line.startswith('#include "'):
                        line = f.readline()
                        continue
                    else:
                        body_lines.append(line)
                    line = f.readline()

        include_lines.add("#include <iostream>\n")
        return list(include_lines), header_lines, body_lines

    def get_default_return(self, stubtype):
        if isinstance(stubtype, JSONContainer):
            pre_return_lines = [
                "result method_result;",
            ]

            pre_return_lines.extend(["method_result.dimension{}Length = 0;".format(str(dim))
                                     for dim in range(1, stubtype.degree + 1)])
            pre_return_lines.append("method_result.array = NULL;")
            return pre_return_lines, "method_result"
        else:
            if stubtype == JSONTypes.INT:
                return [], "0"
            if stubtype == JSONTypes.FLOAT:
                return [], "0.0"
            if stubtype == JSONTypes.STRING:
                return [], '""'
            if stubtype == JSONTypes.CHAR:
                return [], "'\0'"
            if stubtype == JSONTypes.BOOL:
                return [], "false"

    def convert_to_language_type(self, stubtype):
        if isinstance(stubtype, JSONContainer):
            return "{}*".format(self.convert_to_language_type(stubtype.subtype))
        else:
            if stubtype == JSONTypes.INT:
                return "int"
            if stubtype == JSONTypes.FLOAT:
                return "double"
            if stubtype == JSONTypes.STRING:
                return "std::string"
            if stubtype == JSONTypes.CHAR:
                return "char"
            if stubtype == JSONTypes.BOOL:
                return "bool"

    def create_container_return_struct(self, stubtype):
        if not isinstance(stubtype, JSONContainer):
            raise ValueError("Cannot create return struct for non-container type")

        lengths = ["int dimension{}Length;".format(str(dim)) for dim in range(1, stubtype.degree + 1)]

        header = "struct result {"
        length_line = "\n".join(lengths)
        arr_line = "{} array;".format(self.convert_to_language_type(stubtype))
        footer = "};"

        return "result", "{}\n{}\n{}\n{}\n".format(header, length_line, arr_line, footer)

    def make_userimpl_section(self, method_name, return_type, arguments):
        header = ""
        if isinstance(return_type, JSONContainer):
            return_type_str, return_struct_text = self.create_container_return_struct(return_type)
            header += return_struct_text
        else:
            return_type_str = self.convert_to_language_type(return_type)

        arglist = []
        for name, argtype in arguments:
            arglist.append((self.convert_to_language_type(argtype), name))

            if isinstance(argtype, JSONContainer):
                arglist.extend([("int", "{}Dimension{}Length".format(name, str(dim)))
                                for dim in range(1, argtype.degree + 1)])


        arglist = ", ".join(["{} {}".format(langtype, name) for (langtype, name) in arglist])
        header += "{} {}({}) {{\n".format(return_type_str, method_name, arglist)
        pre_return_lines, return_val_str = self.get_default_return(return_type)
        body_lines = [
            "//TODO"
        ]

        body_lines += pre_return_lines
        body_lines.append("return {};".format(return_val_str))

        body = TextStubSection("\n".join(body_lines))
        footer = "}"

        return StubSection(header=header, child_sections=[body], footer=footer)

    def make_main_without_body(self):
        header_lines = self.header_lines
        header_lines.append("int main() {")
        footer = "}"

        return StubSection(header="".join(header_lines), footer=footer)

    def make_parse_input(self):
        lines = [
            "std::string inputContents;",
            "getline(std::cin, inputContents);",
            "JSONList* argList = (JSONList*) JSONParser::get_obj_from_str(inputContents);"
        ]

        return TextStubSection("\n".join(lines))

    def get_container_base_type(self, arrtype):
        while isinstance(arrtype, JSONContainer):
            arrtype = arrtype.subtype

        return self.convert_to_language_type(arrtype)

    def make_array(self, argnum, argument_name, arrtype):
        lines = []
        temp_arrtype = arrtype
        while isinstance(temp_arrtype, JSONContainer):
            jsonlist_name = "{}{}jsonlist".format(
                argument_name, "" if temp_arrtype.degree == 1 else "_dim{}".format(temp_arrtype.degree))
            lines.append("JSONList* {} = NULL;".format(jsonlist_name))
            temp_arrtype = temp_arrtype.subtype

        lines.extend(self.make_array_wrapper(argnum, "argList", argument_name, arrtype))
        return TextStubSection("\n".join(lines))

    def make_array_wrapper(self, argnum, base_list, argument_name, arrtype):
        lang_type = self.convert_to_language_type(arrtype)
        if not isinstance(arrtype, JSONContainer):
            return "{}->get_item({})->cast_data<{}>()".format(base_list, argnum, lang_type)

        jsonlist_name = "{}jsonlist".format(argument_name)
        it_index = "i{}".format(arrtype.degree)
        lines = [
            "{} = (JSONList*) {}->get_item({});".format(jsonlist_name, base_list, argnum),
            "{} {} = {};".format(lang_type, argument_name,
                                 self.make_new_array_str(arrtype, "{}->get_entry_count()".format(jsonlist_name))),
            "for (int {0} = 0; {0} < {1}->get_entry_count(); {0}++) {{".format(it_index, jsonlist_name)
        ]

        subtype = arrtype.subtype
        if not isinstance(subtype, JSONContainer):
            lang_subtype = self.convert_to_language_type(subtype)
            assign_str = "{}->get_item({})->cast_data<{}>()".format(jsonlist_name, it_index, lang_subtype)
        else:
            new_argname = "{}_dim{}".format(argument_name.split("_")[0], arrtype.degree)
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
        return "new {}{}[{}]".format(base_type, "*" * degree_less_one, size_str)

    def make_arg_process(self, argnum, argument_name, argument_type):
        if not isinstance(argument_type, JSONContainer):
            lang_type = self.convert_to_language_type(argument_type)
            return TextStubSection(
                "{} {} = argList->get_item({})->cast_data<{}>();".format(
                    lang_type, argument_name, argnum, lang_type)
            )
        else:
            return self.make_array(argnum, argument_name, argument_type)

    def make_process_output(self, return_type, method_name, arguments):
        lang_ret_type = self.convert_to_language_type(return_type)

        argument_list = []
        for argname, argtype in arguments:
            argument_list.append(argname)

            if isinstance(argtype, JSONContainer):
                for dim in range(1, argtype.degree + 1):
                    argument_list.append("{}{}jsonlist->get_entry_count()"
                                         .format(argname, "" if dim == 1 else 
                                             "_dim{}".format(str(dim))))


        output_str = "{{}} = {}({});".format(method_name, ", ".join(argument_list))

        if isinstance(return_type, JSONContainer):
            lines = [output_str.format("struct result userResult")]
            base_type = self.get_container_base_type(return_type)
            lengths = ["userResult.dimension{}Length".format(str(dim)) for dim in range(1, return_type.degree+1)]
            lines.append("std::cout << Unifiedstr::deep_to_string<{}>((void*)userResult.array, {}, {}) << std::endl;"
                         .format(base_type, return_type.degree, ", ".join(lengths)))

        else:
            lines = [output_str.format(lang_ret_type)]
            lines.append("std::cout << Unifiedstr::to_string(output) << std::endl;")

        return TextStubSection("\n".join(lines))

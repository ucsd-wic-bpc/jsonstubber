class JSONStubber(object):

    def make_stub(self, class_name, method_name, return_type, arguments):
        file_section = self.make_file_without_body(class_name)
        userimpl_section = self.make_userimpl_section(method_name, return_type, arguments)
        main = self.make_main(return_type, method_name, arguments)

        file_section.append_child(userimpl_section)
        file_section.append_child(main)

        return file_section.make()

    def make_file_without_body(self, class_name):
        pass

    def make_userimpl_section(self, method_name, return_type, arguments):
        pass

    def make_main(self, return_type, method_name, arguments):
        main = self.make_main_without_body()
        main.append_child(self.make_parse_input())

        for argnum, argument in enumerate(arguments):
            argument_name, argument_type = argument
            main.append_child(self.make_arg_process(argnum, argument_name, argument_type))

        argument_names = [argument_name for (argument_name, argument_type) in arguments]
        main.append_child(self.make_process_output(return_type, method_name, argument_names))

        return main

    def make_main_without_body(self):
        pass

    def make_parse_input(self):
        pass

    def make_arg_process(self, argnum, argument_name, argument_type):
        pass

    def make_process_output(self, return_type, method_name, arguments):
        pass

    def convert_to_language_type(self, stubtype):
        pass


class StubSection(object):

    def __init__(self, child_sections=None, header=None, footer=None):
        self.child_sections = child_sections or []
        self.header = header or TextStubSection("")
        self.footer = footer or TextStubSection("")

    def append_child(self, child):
        self.child_sections.append(child)

    def make(self):
        children_str = "\n".join([child.make() for child in self.child_sections])
        return "{}\n{}\n{}".format(self.header, children_str, self.footer)

class TextStubSection(object):
    def __init__(self, text):
        self.text = text
        self.children = []

    def append_child(self, child):
        self.children.append(child)

    def make(self):
        return self.text + "\n" + "\n".join([child.make() for child in self.children])

class JSONType(object):
    types = {}

    def __init__(self, description):
        self.description = description
        JSONType.types[description] = self

    @classmethod
    def parse(cls, s):
        return cls.types[s]


class JSONTypes:
    INT = JSONType("int")
    FLOAT = JSONType("float")
    STRING = JSONType("str")
    CHAR = JSONType("char")
    BOOL = JSONType("bool")


class JSONContainer(JSONType):
    def __init__(self, subtype):
        self.subtype = subtype
        self.degree = 1 + (subtype.degree if isinstance(subtype, JSONContainer) else 0)
        super(JSONContainer, self).__init__('list_' + subtype.description)

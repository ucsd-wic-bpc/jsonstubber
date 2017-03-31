from ..pyjsontypes.jsontypes import JSONTypes, JSONContainer
from ..java_stubber import JavaJSONStubber
from ..cpp_stubber import CppJSONStubber
from ..python_stubber import PythonJSONStubber
import os
import sys


root_path = os.path.dirname(sys.argv[0])
root_path_fmt = os.path.join(root_path, "generated", "{}")
unified_str_path = os.path.join(os.path.dirname(root_path), "unifiedstr")
jsonfast_path = os.path.join(os.path.dirname(root_path), "jsonfastparse")

java_stubber = JavaJSONStubber(jsonfastparse_path=jsonfast_path, unifiedstr_path=unified_str_path)
cpp_stubber = CppJSONStubber(jsonfastparse_path=jsonfast_path, unifiedstr_path=unified_str_path)
python_stubber = PythonJSONStubber(jsonfastparse_path=jsonfast_path, unifiedstr_path=unified_str_path)

path_list = [
    (java_stubber, root_path_fmt.format("Problem5.java")),
    (cpp_stubber, root_path_fmt.format("Problem5.cpp")),
    (python_stubber, root_path_fmt.format("Problem5.py")),
]


for stubber, filename in path_list:
    stub = stubber.make_stub("Problem5", "arrayTest", JSONContainer(JSONContainer(JSONContainer((JSONTypes.INT)))),
                             [("Arg1", JSONContainer(JSONContainer(JSONContainer(JSONContainer((JSONTypes.INT)))))),
                             ("Arg2", JSONContainer(JSONContainer(JSONTypes.INT))),
                             ("Arg3", JSONContainer(JSONContainer(JSONTypes.INT)))])

    with open(filename, 'w+') as f:
        f.write(stub)

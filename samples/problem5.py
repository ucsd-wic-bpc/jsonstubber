from json_stubber import JSONTypes, JSONContainer
from java_stubber import JavaJSONStubber
from cpp_stubber import CppJSONStubber
from python_stubber import PythonJSONStubber
java_stubber = JavaJSONStubber()
cpp_stubber = CppJSONStubber()
python_stubber = PythonJSONStubber()

for stubber, filename in [(java_stubber, "Problem5.java"), (cpp_stubber, "Problem5.cpp"),
                          (python_stubber, "Problem5.py")]:
    stub = stubber.make_stub("Problem5", "arrayTest", JSONContainer(JSONContainer(JSONContainer((JSONTypes.INT)))),
                             [("Arg1", JSONContainer(JSONContainer(JSONContainer(JSONContainer((JSONTypes.INT)))))),
                             ("Arg2", JSONContainer(JSONContainer(JSONTypes.INT))),
                             ("Arg3", JSONContainer(JSONContainer(JSONTypes.INT)))])

    with open(filename, 'w+') as f:
        f.write(stub)

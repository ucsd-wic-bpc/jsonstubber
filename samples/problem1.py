from json_stubber import JSONTypes, JSONContainer
from java_stubber import JavaJSONStubber
from cpp_stubber import CppJSONStubber
java_stubber = JavaJSONStubber()
cpp_stubber = CppJSONStubber()

for stubber, filename in [(java_stubber, "Problem1.java"), (cpp_stubber, "Problem1.cpp")]:
    stub = stubber.make_stub("Problem1", "potateAndRoll", JSONTypes.INT, [("hello", JSONTypes.INT)])
    with open(filename, 'w+') as f:
        f.write(stub)

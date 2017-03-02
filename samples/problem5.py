from java_stubber import JavaJSONStubber, JSONTypes, JSONContainer

stubber = JavaJSONStubber()
java = stubber.make_stub("Problem5", "arrayTest", JSONContainer(JSONContainer(JSONContainer((JSONTypes.INT)))),
                         [("Arg1", JSONContainer(JSONContainer(JSONContainer(JSONContainer((JSONTypes.INT)))))),
                         ("Arg2", JSONContainer(JSONContainer(JSONTypes.INT))),
                         ("Arg3", JSONContainer(JSONContainer(JSONTypes.INT)))])

print(java)

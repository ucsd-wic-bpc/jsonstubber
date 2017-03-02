from java_stubber import JavaJSONStubber, JSONTypes, JSONContainer
stubber = JavaJSONStubber()
java = stubber.make_stub("Problem1", "potateAndRoll", JSONTypes.INT, [("hello", JSONTypes.INT)])
print(java)

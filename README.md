jsonstubber
===========
A Python library used to generate stubcode which parses JSON using 
[https://github.com/ucsd-wic-bpc/jsonFASTParse](jsonFASTParse) and sends the
parsed JSON to to-be-implemented method.

This is a standalone project, but is primarily being developed to be used in
[https://github.com/ucsd-wic-bpc/PyCFramework](PyCFramework) to generate templates.

Supported Languages
--------------------
* Java

Usage
-----
```python
from json_stubber import JSONTypes, JSONContainer
from java_stubber import JavaJSONStubber

# Create the stubber
stubber = JavaJSONStubber()

"""
Generate Java code which does the following
1. Accepts a JSON list-string via stdin, where element one is expected to be an
   int, element two is expected to be a float.
2. Parses the JSON list-string using jsonFASTParse
3. Sends the first element and the second element into the (unimplemented) function
   called "userImplementedMethod", which returns an int
"""
generated_java = stubber.make_stub("ClassName", "userImplementedMethod", JSONTypes.INT,
                                   [("arg_one", JSONTypes.INT),
                                    ("arg_two", JSONTypes.FLOAT)])
```

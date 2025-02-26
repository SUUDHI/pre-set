import json
SU={"name":"sudhanshu","age":22,"city":"delhi"}
print(SU)
print(type(SU))

se=json.dumps(SU)#json.dumps() method can be used to convert a Python Dictionary to a JSON string.
print(se)
print(type(se))

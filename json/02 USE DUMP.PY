import json
Emp={"name":"sudhanshu","age":22,"city":"delhi"}
print(Emp)
print(type(Emp))

JEmp=json.dumps(Emp)#json.dumps() method can be used to convert a Python Dictionary to a JSON string.
print(JEmp)
print(type(JEmp))

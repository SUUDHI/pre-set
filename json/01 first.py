import json
emp='{"name":"sudhanshu","age":22,"city":"delhi"}'
print(emp)
print(type(emp))

EMP1=json.loads(emp)#json.loads() method can be used to parse a valid JSON string and convert it into a Python Dictionary.
print(EMP1)
print(type(EMP1))

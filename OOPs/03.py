# class Parent:
#     def __init__(self,value):
#         print("Parent Constructor")
#         self.value = value

#     def func_1(self):
#         print("Parent Show Method")
#         return f"Value is {self.value}"

# class Child(Parent):
#     def __init__(self,value):
#         print("Child Constructor")
#         self.value = "Child Value"
#         super().__init__(value)
#         Parent.__init__(self,value)
#         print(super().func_1())

#     # def func_1(self):
#     #     print("Parent Show Method")
#     #     return f"Value is {self.value}"
    
# obj_1=Child()
# print(obj_1.func_1())
    
class aa:
    def func(self):
        print("aa")

class bb:
    def func(self):
        print("aa")

class cc:
    def func(self):
        print("aa")

aa=[aa(),bb(),cc()]
for data_ in aa:
    print(data_.func())
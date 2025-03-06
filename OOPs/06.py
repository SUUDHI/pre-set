# class A:
#     def spek():
#         print("in class a")

# class B:
#     def spek():
#         print("in class b")

# class C:
#     def spek():
#         print("in class c")

# class D(A,B,C):
#     pass

# obj=D()
# obj.spek()
class A:
    def spek(self):
        print("in class A")

class B:
    def spek(self):
        print("in class B")

class C:
    def spek(self):
        print("in class C")

class D(A, B, C):  # Multiple Inheritance
    pass

obj = D()
obj.spek()

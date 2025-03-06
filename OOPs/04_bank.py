class account:
    __name=None
    __balance=None

    def __init__(self,name,balance):
        self.__name=name
        self.__balance=balance

    def deposit(self,amount):
        self.__balance += amount
        print("Amount deposited successfully")
        print("Your balance is",self.__balance)

    def withdraw(self,amount):
        if amount>self.__balance:
            print("Insufficient balance")
        else:
            self.__balance -= amount
            print("Amount withdraw successfully")
            print("Your balance is",self.__balance)

    def display(self):
        print("Name:",self.__name)
        print("Balance:",self.__balance)

d=account("Rahul",1000)
d.display()

d.deposit(500)
d.withdraw(200)
d.display()
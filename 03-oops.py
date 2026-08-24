"""
    oops - object oriented programming system
    1) Inheritance
    2) Polymoropshim
    3) Encapsulation
    4) Abstraction

    class - collection of "variables" and "functions" (blueprint of object)

    "class" is the "predefined" keyword, used to declare the "class"

    "pass" is the keyword, used to declare the "empty class"

    memory "ocupancy of class" called as "object"  

    for "Instance" multiple copies will create separately  

    __init__() called as constructor

    constructor used to initilize the instance members
"""
# Example-1
# class Test:
#     pass

# obj1 = Test()
# print(id(obj1))

# Example-2
# class Test:
#     num1 = 200
#     num2 = 100

# obj1 = Test()
# x = obj1.num1
# y = obj1.num2
# res = x + y
# print(f"Addition : {res}")


# Example-3
# class Test:
#     def __init__(self,param1,param2):
#         self.num1 = param1
#         self.num2 = param2

# obj1 = Test(200,100)
# x = obj1.num1
# y = obj1.num2
# res = x - y
# print(res)

# Example-4
# class Test:
#     def __init__(vpro,msg):
#         vpro.msg = msg

# obj1 = Test("Good Morning !!!")
# res = obj1.msg
# print(res)


# Example-5 (Instance)
# class Test:
#     num1 = 200

# obj1 = Test()
# obj1.num1 = 2000
# x = obj1.num1
# print(x)

# obj2 = Test()
# res = obj2.num1
# print(res)


# Example-6
# class Test:
#     def __init__(self,msg):
#         self.msg = msg

# obj1 = Test("Hello")
# x = obj1.msg
# print(x)
# obj1.msg = "Hey"

# obj2 = Test("VPro")
# print(obj2.msg)


# Example-7
# class Calculator:
#     def add1(self):
#         num1 = 200
#         num2 = 100
#         res = num1 + num2
#         print(res)

#     def add2(self):
#         num1 = 200
#         num2 = 100
#         res = num1 + num2
#         return res

#     def add3(self,num1,num2):
#         res = num1 + num2
#         print(res)

#     # with para - with return type

# obj1 = Calculator()
# obj1.add1()

# res = obj1.add2()
# print(res)

# obj1.add3(200,100)


# Example-8 (Inheritance) (Parent - Child)
# class Parent:
#     x = 100

# class Child(Parent):
#     y = 200

# obj = Child()
# num1 = obj.x
# num2 = obj.y
# print(num1 + num2)


# Example-9
# class Parent:
#     def __init__(self,param1):
#         self.num1 = param1

# class Child(Parent):
#     def __init__(self, param1,param2):
#         super().__init__(param1)
#         self.num2 = param2

# obj = Child(200,100)
# print(obj.num1 + obj.num2)


# Example-10
# class Parent:
#     
#       def square(self):
#         num1 = 100
#         res = num1 * num1
#         print(res)
#         return res
# class Child(Parent):
#     def cube(self):
#         num1 = 100
#         #res = num1 * num1 * num1
#         res = super().square() * num1
#         print(res)

# class Subchild(Child):
#     def multiplication(self):
#         num1 = 100
#         num2 = 200
#         res = num1 * num2
#         print(res)

# obj = Subchild()
# obj.square()
# obj.cube()
# obj.multiplication()


# Example-11
# class Parent1:
#     num1 = 2000

# class Parent2:
#     num2 = 1000

# class Child(Parent1,Parent2):
#     num3 = 500

# obj = Child()
# print(obj.num1 + obj.num2 + obj.num3)

# Example-12
# class Parent1:
#     num1 = 200
# class Parent2:
#     num1 = 2000
# class Child(Parent2,Parent1):
#     num1 = 20000

# obj = Child()
# print(obj.num1)

# Example-13
# class Parent:
#     def test1(self):
#         print("Hello")

# class Child1(Parent):
#     def test2(self):
#         print("Batch-4")

# class Child2(Parent):
#     def test2(self):
#         print("Python !!!")

# obj = Child1()
# obj.test1()
# obj.test2()

# obj1 = Child2()
# obj1.test1()
# obj1.test2()


# Example-14
# class Parent:
#     x = 100

# class Child1(Parent):
#     y = 200

# class Child2(Parent):
#     y = 2000

# class Subchild(Child2,Child1):
#     z = 20000


# obj = Subchild()
# print(obj.x, obj.y, obj.z)


# Example-15 (method overriding) (polymorphism)
# class Parent:
#     def db_conn(self):
#         print("oracle conn soon...!")

# class Child(Parent):
#     def db_conn(self):
#         print("postgress conn soon...!")


# obj = Child()
# obj.db_conn()


# Example-16 (overloading)
# class Test:
#     def __init__(self):
#         pass
#     def __init__(self, param1):
#         self.param1 = param1
#     def __init__(self, param1,param2):
#         self.param1 = param1
#         self.param2 = param2

# obj = Test(1000,2000)
# print(obj.param1 + obj.param2)


# class Test:
#     def add(self,num1,num2):
#         print(num1+num2)
#     def add(self,num1,num2,num3):
#         print(num1+num2+num3)

# obj = Test()
# obj.add(10,20,30)

# class Test:
#     def add(self,*param1):
#         print( sum(param1) )

# obj = Test()
# obj.add(10,20)
# obj.add(10,20,30)

# private
# unable to access with the help of "objects"
# private members accessable with in the "class"
# __ used to declare the private members

# Example - 17
# class Bank:
#     def __init__(self):
#         self.__balance = 50000

# obj = Bank()
# x = obj.__balance
# print(x)

# Example - 18 (Encapsulation)
# class Bank:
#     def __init__(self,balance):
#         self.__balance = balance

#     def get_balance(self):
#         return self.__balance

#     def set_balance(self,new_balance):
#         self.__balance = new_balance

# obj = Bank(50000)
# print(obj.get_balance())

# obj.set_balance(100000)
# print(obj.get_balance())

# class Test:
#     def __func1(self):
#         print("Hello")

# obj = Test()
# obj.__func1()


# class Test:
#     def __func1(self):
#         print("Hello")
#     def func2(self):
#         self.__func1()

# obj = Test()
# obj.func2()


# Example-19
# class Test:
#     clg_name = "CBIT"   # class level variable

# print(Test.clg_name)

# Example-20
# class Test:
#     clg = "CBIT"    # class variable
#     def __init__(self,name):
#         self.x = name

# obj1 = Test("Std1")
# obj2 = Test("Std2")
# print(obj1.x,Test.clg,sep="--->")
# print(obj2.x,Test.clg,sep="--->")

# Example-21
# class Demo:
#     pass

# obj1 = Demo()

# # add instance variables
# obj1.num1 = 200
# obj1.num2 = 100

# print(obj1.num1 + obj1.num2)    # access instance variable


# Example-22
# class Demo:
#     pass

# Demo.clg = "CBIT"   # add class variable

# print(Demo.clg) # access class variable

# Example-23
# class Demo:
#     pass

# added class varibles
# Demo.num1 = 200
# Demo.num2 = 100

# obj1 = Demo()
# access instance
# print(obj1.num1 + obj1.num2)

# Example-24
# class Demo:
#     pass

# obj1 = Demo()
# obj1.num1 = 200

# Demo.num1 = 2000

# print(obj1.num1)
# print(Demo.num1)

# Example-25
# class Test:
#     clg = "CBIT"

# Test.clg = "CBIT College"

# obj1 = Test()
# print(obj1.clg)


# Exampl-26
# class Test:
#     clg = "CBIT"

#     @classmethod    # decorator
#     def change_clg(cls,new_clg):
#         cls.clg = new_clg

# Test.change_clg("CBIT College")

# print(Test.clg)
# obj1 = Test()
# print(obj1.clg)

# Example-27
# from abc import ABC,abstractmethod
# class Test(ABC):
#     @abstractmethod
#     def add(self):
#         pass

# class Child(Test):
#     def add(self):
#         num1 = 200
#         num2 = 100
#         res = num1 + num2
#         print(res)

# obj = Child()
# obj.add()






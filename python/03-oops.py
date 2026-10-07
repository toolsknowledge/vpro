"""
    oops - object oriented programming system
    1) inheritance
    2) polymorphsim
    3) encapsulation
    4) abstraction

    code reusability
    modularity
    security

    class : collection of variables amnd functions called as class

    "class" is the keyword, used to declare the class
"""

# Example-1
# class Test:
#     num1 = 20
#     num2 = 10

# obj = Test()
# x = obj.num1
# y = obj.num2
# add = x + y
# print(f"Addition : {add}")


# Example-2
# class Test:
#     def __init__(self):
#         self.num1 = 20
#         self.num2 = 10

# obj1 = Test()
# obj1.num1 = 200
# print(obj1.num1 + obj1.num2)

# obj2 = Test()
# print(obj2.num1 + obj2.num2)


# Example-3
# class Test:
#     def __init__(self,num1,num2):
#         self.num1 = num1
#         self.num2 = num2

# obj = Test(20,10)
# print(obj.num1 + obj.num2)

# Example-4
# class Test:
#     # no para - no return
#     def addn1(self):
#         x = 20
#         y = 10
#         res = x + y
#         print(res)

#     # no para - with return
#     def addn2(self):
#         x = 20
#         y = 10
#         res = x + y
#         return res

#     # with para - no return
#     def addn3(self,num1,num2):
#         res = num1 + num2
#         print(res)

#     # with para - with return
#     def addn4(self,num1,num2):
#         res = num1 + num2
#         return res

# obj = Test()
# obj.addn1()


# res = obj.addn2()
# print(res)

# obj.addn3(20,10)

# x = obj.addn4(20,10)
# print(x)


# Inheritance
# getting the data from parent class to child class called as inheritance
# 1) single level. 2) multi-level   3) multiple.  4) Hirarichal     4) Hybrid

# Example-5 (single level)
# class Parent:
#     def __init__(self):
#         self.num1 = 20
# class Child(Parent):
#     def __init__(self):
#         super().__init__()
#         self.num2 = 10
# obj = Child()
# print(obj.num1 + obj.num2)

# Example-6
# class Parent:
#     def __init__(self,a):
#         self.num1 = a
# class Child(Parent):
#     def __init__(self, x,y):
#         super().__init__(x)
#         self.num2 = y
# obj = Child(20,10)
# print(obj.num1 + obj.num2)


# Example-7
# class Parent:
#     def func1(self):
#         print("Hello")
# class Child(Parent):
#     def func2(self):
#         print("Welcome")
# obj = Child()
# obj.func1()
# obj.func2()


# Example-8
# class Parent:
#     def func1(self):
#         print("Hello")
# class Child(Parent):
#     def func2(self):
#         super().func1()
# obj = Child()
# obj.func2()


# Example-9(Multilevel)
# class Parent:
#     def __init__(self):
#         self.num1 = 40
# class Child(Parent):
#     def __init__(self):
#         super().__init__()
#         self.num2 = 30
# class Subchild(Child):
#     def __init__(self):
#         super().__init__()
#         self.num3 = 20
# class GrandChild(Subchild):
#     def __init__(self):
#         super().__init__()
#         self.num4 = 10
# obj = GrandChild()
# print(obj.num1 + obj.num2 + obj.num3 + obj.num4)

# Example-10 (Multiple)
# class Parent1:
#     def __init__(self):
#         self.num1 = 300
# class Parent2:
#     def __init__(self):
#         self.num2 = 200
# class Child(Parent1,Parent2):
#     def __init__(self):
#         Parent1.__init__(self)
#         Parent2.__init__(self)
#         self.num3 = 100
# obj = Child()
# print(obj.num1 + obj.num2 + obj.num3)


# Example-11
# class Parent1:
#     def __init__(self):
#         self.num1 = 1000
# class Parent2:
#     def __init__(self):
#         self.num1 = 100
# class Child(Parent1,Parent2):
#     def __init__(self):
#         Parent2.__init__(self)
#         Parent1.__init__(self)
#         self.num2 = 10
# obj = Child()
# print(obj.num1, obj.num2)



# Example-12 (Hirarichal Inheritance)
# class Parent:
#     def __init__(self):
#         self.num1 = 200

# class Child1(Parent):
#     def __init__(self):
#         super().__init__()
#         self.num2 = 100

# class Child2(Parent):
#     def __init__(self):
#         super().__init__()
#         self.num2 = 10

# obj1 = Child1()
# print(obj1.num1, obj1.num2)

# obj2 = Child2()
# print(obj2.num1, obj2.num2)

# Example-13
# Hybrid Inheritance
# class Test1:
#     def __init__(self):
#         self.num1 = 40

# class Test2(Test1):
#     def __init__(self):
#         super().__init__()
#         self.num2 = 30

# class Test3(Test1):
#     def __init__(self):
#         super().__init__()
#         self.num3 = 20

# class Test4(Test2,Test3):
#     def __init__(self):
#         Test2.__init__(self)
#         Test3.__init__(self)
#         self.num4 = 10

# obj = Test4()
# print(obj.num1, obj.num2, obj.num3, obj.num4)


# Example-14
# overloading : same function names, but different parameters list called as overloading
# polymorphism
# overloading not supported by python 
# class Test:
#     def add(self,num1,num2):
#         print(num1+num2)
#     def add(self,num1,num2,num3):
#         print(num1+num2+num3)
#     def add(self,num1,num2,num3,num4):
#         print(num1+num2+num3+num4)
# obj = Test()
# obj.add(10,20,30,40)


# Example-15
# achieving overloading with the help of variable-length parameter
# class Test:
#     def add(self,*nums):
#         print(sum(nums))

# obj = Test()
# obj.add(10,20)
# obj.add(10,20,30)
# obj.add(10,20,30,40)
# obj.add(10,20,30,40,50)

# Example-16
# class Test:
#     def __init__(self):
#         pass
#     def __init__(self, param1):
#         pass
#     def __init__(self, param1,param2):
#         pass
# obj = Test(10,20)


# Example-17
# Overriding : overriding parent class functionality with child class functionality
# Polymorphsim
# Inheritance
# both Parent and Child must contain same function
# class Parent:
#     def dbfunc(self):
#         print("Oracle Conn Soon...!")
# class Child(Parent):
#     def dbfunc(self):
#         print("VectorDB Conn Soon...!")

# obj = Child()
# obj.dbfunc()


# Example-18
# class Bank:
#     def __init__(self):
#         self.__balance = 1000       # __, used to declare the private variables
                                    # "unable" to access with the help of objects
                                    # private variables "unable" to access to child classes also
                                    # private variables, able to access with in the same class
# obj = Bank()
# obj.__balance               

# class Axis(Bank):
#     pass

# obj = Axis()
# obj.__balance


# Example-19
# Encapsulation
# class Bank:
#     def __init__(self):
#         self.__bal = 1000
#     def setBal(self):
#         self.__bal = 10000 
#     def getBal(self):
#         return self.__bal
# obj = Bank()
# obj.setBal()
# print(obj.getBal())


# Example-20
# from abc import ABC,abstractmethod
# class Test(ABC):
#     @abstractmethod
#     def start_busiess(self):
#         pass

# class Frnd1(Test):
#     def start_busiess(self):
#         print("Start EduTech")

# class Frnd2(Test):
#     def start_busiess(self):
#         print("Start Development")

# obj = Frnd1()
# obj.start_busiess()


# Example-21
# """
#     we are able to call functions as "variables" with the help @property
# """
# class Test:
#     @property
#     def func1(self):
#         print("Hello")

# obj = Test()
# obj.func1


# Example-22
# class Test:
#     # class level variable
#     name = "Hello"

# print(Test.name)


# Example-23
# class Test:
#    name = "Hello" 
   

# obj = Test()
# print(obj.name)     # accessing instance variable, but we dont have any instance variable, so priority goes to class variable


# Example-24
# class Test:
#     name = "Hello"
#     def __init__(self):
#         self.x = 200
#         self.y = 100

# print(Test.__dict__)
# obj = Test()
# print(obj.__dict__)


# Example-25
# class Test:
#     # class level variable
#     name = "Hello"
#     # class level function
#     # cls (rename possible)
#     def test_func(cls):
#         cls.name = "Welcome"

# # call class level function
# Test.test_func(Test)
# print(Test.name)

# Example-26
# class Company:
#     @staticmethod
#     def cafetaria():
#         print("Accessable to all Dept !!!")

# Company.cafetaria()

# self - instance
# cls - class
# --  - static method


# """
#     additing additional functionality called as decorator
#     we will use decorator with "@"
# """
# Example-27
# def add_initial(func):
#     def wrapper():
#         print("Mr.",end=" ")
#         func()
#     return wrapper

# @add_initial
# def display():
#     print("Samba")

# display()


# Example-28 (MRO) (Subchil -- Child --- Parent)
# class Parent:
#     def display(self):
#         print("Parent !!!")

# class Child(Parent):
#     pass

# class Subchild(Child):
#     pass

# obj = Subchild()
# obj.display()
# print(Subchild.mro())
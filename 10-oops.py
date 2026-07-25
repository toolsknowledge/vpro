# OOPS (Object Oriented Programming System)
# collection of variables(properties) and functions(behaviours) called as "class"
# "class" is the keyword, used to declare the "classes"
# "pass" is the keyword, used to declare the empty class
# sharing same copy to multiple objects called as "instance members"
# "self" is the keyword, used to declare the "instance members"
# 1) inheritance        2) polymorphsim      3) encapsulation        4) abstraction

# Example - 1 
# class Test:
#     pass

# obj1 = Test()       # constructor calling
# print(obj1)
# print(id(obj1))


# Example - 2 (Instance Member)
# class Test:
#     num1 = 100

# obj1 = Test()
# obj1.num1 = 1000

# obj2 = Test()
# print(obj2.num1)


# Example - 3
# class Test:
#     num1 = 200
#     num2 = 100

# obj1 = Test()
# add = obj1.num1 + obj1.num2
# print(add)

# Example - 4
# class Test:
#     def test1(self):
#         print("Hello")
    
#     def test2(self):
#         return "Hello"
    
#     def test3(self,param1):
#         print(param1)

#     def test4(self,param1):
#         return param1

# obj1 = Test()
# obj1.test1()

# res1 = obj1.test2()
# print(res1)

# obj1.test3("Hello")

# res2 = obj1.test4("Hello")
# print(res2)


# Example - 5
# class Test:
#     def __init__(self,num1,num2):
#         self.num1 = num1
#         self.num2 = num2

# obj1 = Test(200,100)
# add = obj1.num1 + obj1.num2
# print(add)


# Example - 6
# class Test:
#     def __init__(self,num1):
#         self.num1 = num1

#     def test1(self):
#         print(self.num1)

#     def test2(self):
#         return self.num1



# obj1 = Test(200)
# obj1.test1()
# res1 = obj1.test2()
# print(res1)

# Inheritance
# getting the properties and behaviours from parent class to child class
# 1) single level       2) multi level      3) multiple     4) hirarichal       5) hybrid

# Example-7
# class Parent:
#     def __init__(self):
#         self.name = "VPro"

# class Child(Parent):
#     pass

# obj = Child()
# print(obj.name)

# Example-8
# class Parent:
#     def test1(self):
#         print("Parent !!!")
# class Child(Parent):
#     def test2(self):
#         print("Child !!!")
# class Subchild(Child):
#     def test3(self):
#         print("Subchild !!!")


# obj = Subchild()
# obj.test1()
# obj.test2()
# obj.test3()

# Example - 9
# class Parent1:
#     def test1(self):
#         print("Parent1 !!!")

# class Parent2:
#     def test1(self):
#         print("Parent2 !!!")

# class Child(Parent2,Parent1):
#     pass

# obj = Child()
# obj.test1()
# obj.test2()

# obj.test1()


# Example - 10 (Hirarichal)
# class Parent:
#     def __init__(self):
#         self.x = 100

# class Child1(Parent):
#     def __init__(self):
#         super().__init__()
#         self.y = 200

# class Child2(Parent):
#     def __init__(self):
#         super().__init__()
#         self.y = 300

# Obj1 = Child1()
# print(Obj1.x,"......",Obj1.y)

# Obj2 = Child2()
# print(Obj2.x,"......",Obj2.y)


# Example - 11 (Hybrid - Hirarichal + Multiple)
# class Parent:
#     def __init__(self):
#         self.x = 100

# class Child1(Parent):
#     def __init__(self):
#         super().__init__()
#         self.y = 200

# class Child2(Parent):
#     def __init__(self):
#         super().__init__()
#         self.y = 300

# class Subchild(Child1,Child2):
#     def __init__(self):
#         super().__init__()
#         self.a = 400

# obj = Subchild()
# print(obj.x, obj.y, obj.a)


# Example - 12
# super() - child class will call parent class members with the help of super()
# class Parent:
#     def __init__(self,param1):
#         self.num1 = param1

# class Child(Parent):
#     def __init__(self, param1,param2):
#         super().__init__(param1)
#         self.num2 = param2

# obj = Child(200,100)
# print(obj.num1, obj.num2)


# Example - 13
# class Parent:
#     def test(self):
#         print("Parent !!!")

# class Child(Parent):
#     def wish(self):
#         super().test()

# obj = Child()
# obj.wish()


# Example-14
# class Parent:
#     def __init__(self):
#         self.__x = 100

# class Child(Parent):
#     pass

# obj = Child()
# print(obj.__x)

# Example - 15
# class Parent:
#     def __test(self):
#         print("Hello")

#     def wish(self):
#         self.__test()

# class Child(Parent):
#     pass

# obj = Child()
# obj.wish()

# Example - 16
# Overriding - overriding Parent functionality with Child class functionality called as function overriding
# Overriding comes under polymorphsim

# class Parent:
#     def db_func(self):
#         return "MySQL Conn Soon....!"

# class Child(Parent):
#     def db_func(self):
#         return "MongoDB Conn Soon....!"

# obj1 = Child()
# print(obj1.db_func())

# Example - 17
# Overloadng - "same function name" with multiple parameters called as Overloading

# class Test:
#     def add(self,num1,num2):
#         res = num1 + num2
#         print(res)

#     def add(self,num1,num2,num3):
#         res = num1 + num2 + num3
#         print(res)

#     def add(self,num1,num2,num3,num4):
#         res = num1 + num2 + num3 + num4
#         print(res)

# obj = Test()
# obj.add(100,200,300,400)

# class Test:
#     def add(self,*nums):        # tuple - able to hold more than one paramere
#         print(sum(nums))        # overloading

# obj = Test()
# obj.add(10,20)
# obj.add(10,20,30)
# obj.add(10,20,30,40)


# Example - 18 (Class Level)
# class Test:
#     college = "CBIT !!!"


# print( Test.college )

# obj1 = Test()
# print(obj1.college)

# obj2 = Test()
# print(obj2.college)

# Example - 19
# class Test:
#     college = "CBIT !!!"

#     def __init__(self):
#         self.college = "KLU !!!"

# print(Test.college)
# obj = Test()
# print(obj.college)


# Example - 20
# class Test:
#     pass

# obj = Test()
# obj.x = 100 # adding instance variable

# print(obj.x) # accessing instance variable

# Example - 21
# class Test:
#     name = "Hello"

# Test.name = "Gen AI"
# print(Test.name)

# Example - 22
# class Test:
#     name = "Hello"
#     def test_func(cls):
#         cls.name = "Agentic AI"

# Test.test_func(Test)
# print(Test.name)

# Example - 23
# from abc import ABC,abstractmethod
# class Test(ABC):
#     @abstractmethod
#     def my_func(self):
#         pass

# class Test1(Test):
#     def my_func(self):
#         print("Hello")

# obj = Test1()
# obj.my_func()


# Example - 24
# from abc import ABC,abstractmethod
# class Business(ABC):
#     @abstractmethod
#     def start_business(self):
#         pass

# class Frnd1(Business):
#     def start_business(self):
#         return "start dev center"

# class Frnd2(Business):
#     def start_business(self):
#         return "start edu tech company"

# obj1 = Frnd1()
# print(obj1.start_business())

# obj2 = Frnd2()
# print(obj2.start_business())


# Revise - 1
# class Test:
#     cmp = "TCS"

# print(Test.cmp)

# Revise - 2
# class Test:
#     cmp = "TCS !!!"

#     def __init__(self):
#         self.cmp = "Infosys !!!"

# obj1 = Test()
# print(obj1.cmp)

# print(Test.cmp)

# Revise - 3
# class Test:
#     cmp = "TCS !!!"

# obj = Test()
# print(obj.cmp)


# Revise - 4
# class Test:
#     pass

# obj = Test()
# obj.cmp = "TCS !!!"

# print(obj.cmp)


# Revise - 5
# class Test:
#     cmp = "TCS !!!"

# Test.cmp = "Infosys"

# obj = Test()
# print(obj.cmp)


# Revide - 6
# class Test:
#     cmp = "TCS !!!"

#     def hello(cls):
#         cls.cmp = "Infosys !!!"

# Test.hello(Test)
# print(Test.cmp)


# Revise - 7
# class Test:
#     cmp = "TCS !!!"

#     def hello(cls,new_cmp):
#         cls.cmp = new_cmp

# Test.hello(Test,"Infosys !!!")
# print(Test.cmp)


# protected
# class Bank:
#     def __init__(self):
#         self._balance = 10000

# obj = Bank()

# class Other:
#     def __init__(self,my_obj):
#         self.x = my_obj

# other_obj = Other(obj)
# print(other_obj.x._balance)

# Encapsulation - wrapping the properties and behaviour
# "class" keyword
# class Test:
#     cmp = "TCS !!!"

#     def __init__(self):
#         self.cmp = "Infosys !!!"

#     def func_one(self):
#         pass

#     def func_two(cls):
#         pass
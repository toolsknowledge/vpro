"""
    oops
    ****
        oops stands for "object oriented programming system"
        by using oops, we are able to
        1) reuse
        2) modularity
        3) abstraction
        --
        --
        --

        oops concepts
        1) inheritance
        2) polymorphism
        3) abstraction
        4) encapsulation

        class - collection of variables and functions called as class
        "class" is the keyword, used to create the classes
        we are able to create "object" to class

        instance:
            we are able to create multiple objects
            all object are separate copies in memory
            "self" is the predefined "word", used to recognize the instance member
            we are able to rename "self"

        constructors are used to initilize the instance members dynamically
        __init__(), used to create the constructors in python
"""

# Example-1
# class Test:
#     pass

# obj1 = Test()
# print(id(obj1))

# Example-2
# class Test:
#     num1 = 200

# obj1 = Test()
# obj1.num1 = 2000

# obj2 = Test()
# x = obj2.num1
# print(x)


# Example-3
# class Calculator:
#     num1 = 200
#     num2 = 100

# obj1 = Calculator()
# x = obj1.num1
# y = obj1.num2
# add = x + y
# print(f"Addition | {add}")

# Example-4
# class Test:
#     def __init__(self,param1,param2):
#         self.num1 = param1
#         self.num2 = param2

# obj1 = Test(200,100)
# x = obj1.num1
# y = obj1.num2
# add = x + y
# print("Addition : {}".format(add))

# Example-5
# class Test:
#     def __init__(vpro,msg):
#         vpro.msg = msg

# obj1 = Test("Hello, VPro !!!")
# x = obj1.msg
# print(x)


# Example-6
# class Test:
#     def add(self):
#         num1 = 200
#         num2 = 100
#         res = num1 + num2
#         print(f"Addition : {res}")

#     def sub(self):
#         num1 = 200
#         num2 = 100
#         res = num1 - num2
#         print(f"Subtraction : {res}")

# obj1 = Test()
# obj1.add()
# obj1.sub()


# Example-7
# class Calculator:
#     # no para - no return type
#     def square1(self):
#         res = 10 * 10
#         print(res)
#     # with para - no return
#     def square2(self,num1):
#         res = num1 * num1
#         print(res)
#     # no para - with return type (square3)

#     # with para - with return type (square4)

# obj1 = Calculator()
# obj1.square1()
# obj1.square2(20)

# Cube of a number (Assignment)



# Example-9
# class Parent:
#     num1 = 200
# class Child(Parent):
#     num2 = 100

# obj1 = Child()
# x = obj1.num1
# y = obj1.num2
# res = x + y
# print(res)


# Example-10
# class Parent:
#     def __init__(self,a):       # a = 200, because of line "146"
#         self.num1 = a           # num1 = 200

# class Child(Parent):
#     def __init__(self, x,y):        # x = 200, y = 100 because of line "149"
#         super().__init__(x)
#         self.num2 = y               # num2 = 100

# obj1 = Child(200,100)
# x = obj1.num1
# y = obj1.num2
# res = x + y
# print(res)


# Example-11
# class Parent:
#     def add(self):
#         print("Welcome to add function !!!")

# class Child(Parent):
#     def sub(self):
#         print("Welcome to sub function !!!")

# obj = Child()
# obj.add()
# obj.sub()

# Example-12
# class Parent:
#     num1 = 400

# class Child(Parent):
#     num2 = 300

# class Subchild(Child):
#     num3 = 200

# class GrandChild(Subchild):
#     num4 = 100

# create object to GrandChild
# access 4 variable


# Example-13
# class Parent1:
#     num1 = 300
# class Parent2:
#     num2 = 200
# class Child(Parent1,Parent2):
#     num3 = 100


# Example-14
# class Parent1:
#     num1 = 100
# class Parent2:
#     num1 = 1000
# class Child(Parent2,Parent1):
#     num1 = 200

# obj = Child()
# print(obj.num1)


# Example-15
# class Parent:
#     def func1(self):
#         print("Hello, func1 !!!")

# class Child1(Parent):
#     def func2(self):
#         print("Hello, func2 from Child1 !!!")

# class Child2(Parent):
#      def func2(self):
#             print("Hello, func2 from Child2 !!!")

# create obj to Child1
# create obj to Child2

# Example-16
# class Parent:
#     a = 400

# class Child1(Parent):
#     b = 300

# class Child2(Parent):
#     c = 200

# class Subchild(Child1,Child2):
#     d = 100


# Example-17
# overriding parent class functionality with child child class functionality called as function overriding
# function overriding comes under polymorphsim
# function overriding technically called as dynamic polymorphism
# rule : both parent & child must have same function name
# class Parent:
#     def property(self):
#         print("2BHK-House !!!")
# class Child(Parent):
#     def property(self):
#         print("3 BHK House !!! + Car + Land")
# obj = Child()
# obj.property()


# Example - 18
# same "function name" with "different parameters" called as function overloading
# function overloading not supported by python
# function overloading also comes under polymorphism
# function overloading also called as static polymorphsim
# class Test:
#     def add(self,num1,num2):
#         print(num1+num2)
#     def add(self,num1,num2,num3):
#         print(num1+num2+num3)
#     def add(self,num1,num2,num3,num4):
#         print(num1+num2+num3+num4)
# obj = Test()
# obj.add(40,30,20,10)

# Example-19
# class Test:
#     def add(self,*nums):
#         print(sum(nums))
# obj = Test()
# obj.add(10,20)
# obj.add(10,20,30)
# obj.add(10,20,30,40)

# Example-20
# class Test:
#     def __init__(self):
#         pass
#     def __init__(self, param1):
#         print(param1)
#     def __init__(self, param1,param2):
#         print(param1, param2)
# obj = Test(200,100)

# Example-21
# class Test:
#     def __init__(self,*nums):
#         print(sum(nums))

# Test(20,10,5,1)

# Example-22
# class Bank:
#     def __init__(self):
#         self.__balance = 2000

# obj = Bank()
# print(obj.balance)

# Example-23
# class Parent:
#     def __init__(self):
#         self.__num = 1000

# class Child(Parent):
#     pass

# obj = Child()
# obj.__num


# Example-24
# we can't access private members with the help of objects
# private members wont accessable to child classes
# we will create private members with the help of __
# we can acccess private members with the help of "public functions" with in the same class
# Encapsulation
# class Test:
#     def __init__(self,param1):
#         self.__x = param1
#     def getX(self):
#         return self.__x
#     def setX(self,new_x):
#         self.__x = new_x

# obj = Test(100)
# obj.setX(1000)
# print( obj.getX() )


# Example-25
# class Test:
#     college_name = "CBIT"

# obj1 = Test()
# obj2 = Test()
# obj3 = Test()
# print(obj1.college_name)
# print(obj2.college_name)
# print(obj3.college_name)

# Example-26
# class Test:
#     # class level variable
#     college_name = "CBIT"

#     def __init__(self):
#         # instance variable
#         self.college_name = "Vasavi"

# obj = Test()
# print(obj.college_name)

# Example-27
# class Test:
#     college_name = "CBIT"
#     def __init__(self):
#         self.college_name = "Vasavi"
# print(Test.college_name)


# Revision
# class Test:
#     # class level variable
#     num1 = 200
#     num2 = 100
#     def __init__(self):
#         # instance variables
#         self.num1 = 2000
#         self.num2 = 1000

# obj = Test()
# print(obj.num1 + obj.num2)
# print(Test.num1 + Test.num2)

# Example-28
# class Test:
#     pass

# obj = Test()
# obj.x = 100

# # print(obj.x)
# print(Test.x)

# Example-29
# class Test:
#     pass

# Test.msg = "Hello"
# print(Test.msg)
# obj = Test()
# print(obj.msg)

# Example-30
# class Test:
#     name = "Hello"

# Test.name = "Welcome"
# print(Test().name)


# Example-31
# class Test:
#     name = "Hello"
    
#     @classmethod
#     def test_func(cls):
#         cls.name = "Welcome"

# Test.test_func()
# print(Test.name)












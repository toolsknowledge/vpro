"""
    oops - object oriented programming system
    1) reusability
    2) modularity
    3) security
    4) readability

    oops
    ****
    1) inheritance
    2) polymorphism
    3) encapsulation
    4) abstraction

    class
    *****
        collection of "variables" and "functions" called as "class"
        "class" is the keyword, used to define the "class"
        we are able to create "object" to the class
"""

# Example-1
# class Test:
#     num1 = 200
#     num2 = 100

# obj = Test()
# x = obj.num1
# y = obj.num2
# add = x + y
# print(f"Addition : {add}")      # Addition : 300


"""
    instance
    ********
        we are able to create multiple objects
        one object manippulations wont effect to other objects
        "self" is the predefined word, used to refer the current object
        we are able to rename "self"

        __init__() is the contrsuctor
        constructor, used to initilize the "instance members"
"""
# Example-2
# class Test:
#     def __init__(self):
#         self.num1 = 200
#         self.num2 = 100

# obj1 = Test()
# obj1.num1 = 2000
# obj1.num2 = 1

# obj2 = Test()
# x = obj2.num1
# y = obj2.num2
# print(x, y)


# Example-3
# initilize instance members dynamically (constructor)
# class Test:
#     def __init__(self,num1,num2):
#         self.num1 = num1
#         self.num2 = num2

# obj1 = Test(200,100)
# a = obj1.num1
# b = obj1.num2
# add = a + b
# print(add)


# Example-4
# class Company:
#     def __init__(x,emp_name,emp_id):
#         x.emp_name = emp_name
#         x.emp_id = emp_id

# c1 = Company("Emp1",101)
# print(c1.emp_name, c1.emp_id)

# c2 = Company("Emp2",102)
# print(c2.emp_name, c2.emp_id)



# Example-5
# class Test:
#     # instance function
#     # no parameter - no return
#     def power1(self):
#         num1 = 10
#         res = num1 ** num1
#         print(res)

#     # instance function
#     # no parameters - with return
#     def power2(self):
#         num1 = 1
#         res = num1 ** num1
#         return res

#     # instance function
#     # with parameter - no return
#     def power3(self,num1):
#         res = num1 ** num1
#         print(res)

#     # instance function
#     # with parameter - with return 
#     def power4(self,num1):
#         res = num1 ** num1
#         return res

# obj1 = Test()
# obj1.power1()       # 10000000000

# x = obj1.power2()
# print(x)

# obj1.power3(2)

# y = obj1.power4(3)
# print(y)

# no para - no return type
# no para - with return
# with para - no return
# with para - with return


# Example-6
# class Test:
#     # instannce variables
#     def __init__(self,msg):
#         self.msg = msg

#     def wish(self):
#         print(self.msg)


# obj = Test("Morning !!!")
# obj.wish()


# Example-7
# python wont support multiple constructors (overloading)
# internally overriding will happen
# class Test:
#     def __init__(self):
#         pass
#     def __init__(self, param1):
#         pass
#     def __init__(self, param1,param2):
#         pass


"""
    inheritance
        getting the data from "parent" class to child "class" called as inheritance
        1) single level
        2) multi level
        3) multiple
        4) hirarichal
        5) hybrid
"""

# Example-8
# Single Level
# class Parent:
#     def __init__(self):
#         self.num1 = 20

# class Child(Parent):
#     def __init__(self):
#         super().__init__()
#         self.num2 = 10

# obj = Child()
# print(obj.num1 + obj.num2)


"""
    child class will communicate with parent class with super()
"""
# Example-9
# class Parent:
#     def __init__(self,num1):
#         self.num1 = num1

# class Child(Parent):
#     def __init__(self, num1,num2):
#         super().__init__(num1)
#         self.num2 = num2

# obj = Child(20,10)
# print(obj.num1 + obj.num2)


# Example-10
# class Parent:
#     def func1(self):
#         print("Hello")

#     def func2(self):
#         print("Python")

# class Child(Parent):
#     def func3(self):
#         print("AgenticAI")
#     def func4(self):
#         super().func1()

# obj = Child()
# obj.func1()
# obj.func2()
# obj.func3()
# obj.func4()

# Example-11
# class Parent:
#     def __init__(self):
#         self.x = "Frontend"
# class Child(Parent):
#     def __init__(self):
#         super().__init__()
#         self.y="Backend"
# class Subchild(Child):
#     def __init__(self):
#         super().__init__()
#         self.z = "DataBase"
# obj = Subchild()
# print(obj.x,obj.y,obj.z,sep="-->")


# Example-12
# Multiple
# class Parent1:
#     def __init__(self):
#         self.num1 = 30

# class Parent2:
#     def __init__(self):
#         self.num2 = 20

# class Child(Parent1,Parent2):
#     def __init__(self):
#         Parent1.__init__(self)
#         Parent2.__init__(self)
#         self.num3 = 10

# obj = Child()
# print(obj.num1 + obj.num2 + obj.num3)


# Example-13
# class Parent1:
#     def __init__(self):
#         self.num1 = 1000
# class Parent2:
#     def __init__(self):
#         self.num1 = 2000
# class Child(Parent1,Parent2):
#     def __init__(self):
#         Parent1.__init__(self)
#         Parent2.__init__(self)
#         self.num2 = 500
# print(Child().num1, Child().num2)


# Example-14
# Hirarichal
# class Parent:
#     def func1(self):
#         print("Python !!!")

# class Child1(Parent):
#     def func2(self):
#         print("Gen AI !!!")

# class Child2(Parent):
#     def func2(self):
#         print("Agentic AI !!!")

# Child2().func1() 
# Child2().func2()

# Child1().func1()
# Child1().func2()



# Example-15
# hybrid
# class Parent:
#     def __init__(self):
#         self.num1 = 1

# class Child1(Parent):
#     def __init__(self):
#         super().__init__()
#         self.num2 = 2

# class Child2(Parent):
#     def __init__(self):
#         super().__init__()
#         self.num3 = 3

# class Child3(Child1,Child2):
#     def __init__(self):
#         super().__init__()
#         self.num4 = 4
# obj3 = Child3()
# print(obj3.num1, obj3.num2, obj3.num3, obj3.num4)


"""
    __, used to create private members
    unable to access with the help of objects
    unable to access in child classes also
    private members accessable with in the same class
"""
# Example-16
# class Account:
#     def __init__(self):
#         self.__bal = 1000

# class Bank(Account):
#     pass

# obj = Account()
# obj.__bal

# obj = Bank()
# obj.__bal


# Example-17
# class Account:
#     def __init__(self):
#         self.__bal = 1000 

#     def get_bal(self,passcode):
#          if passcode == "vpro@123":
#              print(self.__bal)
#          else:
#             print("Unauthoprized Access")

# obj = Account()
# obj.get_bal("vpro@1234")



# Example-18 (Encapsulation)
# class Test:
#     def __init__(self,num):
#         self.__num = num

#     def set_num(self,num):
#         self.__num = num

#     def get_num(self):
#         print(self.__num)

# obj = Test(100)
# obj.get_num()

# change private variable
# obj.set_num(200)
# access private variable
# obj.get_num()


# Example-19
# same function name, but different parameters called as function overrloading
# python wont supports function overloading
# function overloading comes under "polymorphism"
# with the help of variable-lenght (tuple) , we can achieve overloading

# class Test:
#     def addn(self,num1,num2):
#         res = num1 + num2
#         print(res)
#     def addn(self,num1,num2,num3):
#        res = num1 + num2 + num3
#        print(res)

# obj = Test()
# obj.addn(10,20,30)

# Example-20
# class Test:
#     def addn(self,*num):
#         print(sum(num))

# obj = Test()
# obj.addn(10,20)
# obj.addn(100,200,300)
# obj.addn(1,2,3,4)



# Example-21
# overriding parent class functionality with child class, called as function overriding
# overriding is the part of polymorphsim
# to achieve function overriding, inheritance mandatory
# both parent and child must contain same function name

# class Parent:
#     def property(self):
#         return "2bhk house"

# class Child(Parent):
#     def property(self):
#         return "3bhk house + car"

# obj = Child()
# print( obj.property() )



# Example-22
# function without implementation called as abstraction
# @abstractmethod and ABC
# child classes will provide implementation

# from abc import ABC,abstractmethod
# class Test(ABC):
#     @abstractmethod
#     def start_business(self):
#         pass

# class Frnd1(Test):
#     def start_business(self):
#         print("---Startup---")

# class Frand2(Test):
#     def start_business(self):
#         print("---Training----")

# obj = Frand2()
# obj.start_business()

# obj1 = Frnd1()
# obj1.start_business()

# Example-23
# property is the predefined decorator
# by using property, we are able to call functions like variables

# class Test:
#     @property
#     def addn(self):
#         num1 = 10
#         num2 = 20
#         res = num1 + num2
#         print(res)

# obj = Test()
# obj.addn


# Example-24
class Test:
    name = "CBIT"

# print(Test.name)
obj = Test()
print(obj.name)     # __init__()


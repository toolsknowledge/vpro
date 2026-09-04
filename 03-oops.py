"""
    collection of variables and functions called as class
    "class" is the keyword, used to define the classes
    "pass" is the keyword, used to define empty class
    we are able to create object to "classes"

    instance:
    ********
        multiple copies will create internally(memory)(ram)
        one object changes wont effect to any other objects
        self is used to define instance members
"""

# class Test:
#     pass

# obj1 = Test()
# print(id(obj1))


# class Test:
#     num1 = 200

# obj1 = Test()
# obj1.num1 = 2000
# x = obj1.num1
# print(x)

# obj2 = Test()
# y = obj2.num1
# print(y)

# class Test:
#     num1 = 200
#     num2 = 100

# obj1 = Test()
# x = obj1.num1
# y = obj1.num2
# add = x + y
# print(f"Addition :{add}")


# class Test:
#     def __init__(self,param1,param2):
#         self.num1 = param1
#         self.num2 = param2

# obj1 = Test(200,100)
# x = obj1.num1
# y = obj1.num2
# print(x+y)


# class Test:
#     def __init__(vpro,msg):
#         vpro.wish = msg

# obj1 = Test("Hello")
# x = obj1.wish
# print(x)


# class Test:
#     def add1(self):
#         num1 = 200
#         num2 = 100 
#         res = num1 + num2
#         print(res)
#     def add2(self,param1,param2):
#         res = param1 + param2
#         return res
#     # no para with return
#     # with para - no return 

# obj1 = Test()
# obj1.add1()
# x = obj1.add2(200,100)
# print(x)



# getting data from parent class to child class called as inheritance
# super() is used to call parent class members from child classes (variables, functions and constructors)
# class Parent:
#     num1 = 200

# class Child(Parent):
#     num2 = 100

# obj1 = Child()
# x = obj1.num1
# y = obj1.num2
# print(x+y)


# class Parent:
#     def __init__(self,param1):
#         self.num1 = param1 

# class Child(Parent):
#     def __init__(self, param1,param2):
#         super().__init__(param1)
#         self.num2 = param2

# obj1 = Child(200,100)
# x = obj1.num1
# y = obj1.num2
# print(x+y)


# class Parent:
#     def test1(self):
#         num1 = 200
#         return num1
# class Child(Parent):
#     def test2(self):
#         num2 = 100
#         return num2
# obj1 = Child()
# print(obj1.test1() + obj1.test2())

# class Parent:
#     def test1(self):
#         return 200
# class Child(Parent):
#     def test2(self):
#         return super().test1() + 100
# obj1 = Child()
# print(obj1.test2())


# class Parent:
#     def __init__(self,x):
#         self.x = x
# class Child(Parent):
#     def __init__(self, x,y):
#         super().__init__(x)
#         self.y = y
# class Subchild(Child):
#     def __init__(self, x, y,z):
#         super().__init__(x, y)
#         self.z = z

# obj1 = Subchild(300,200,100)
# print(obj1.x + obj1.y + obj1.z)

# class Parent1:
#     def test1(self):
#         return "test1"
# class Parent2:
#     def test2(self):
#         return "test2"
# class Child(Parent1,Parent2):
#     def test3(self):
#         return "test3"
# obj1 = Child()
# print(obj1.test1(),obj1.test2(), obj1.test3())

# class Demo1:
#     def test1(self):
#         return 300
# class Demo2:
#     def test1(self):
#         return 3000
# class Demo3(Demo2,Demo1):
#     def test2(self):
#         return 30000
# obj1 = Demo3()
# print(obj1.test2() + obj1.test1())


# class Parent:
#     num1 = 200
# class Child1(Parent):
#     num2 = 2000
# class Child2(Parent):
#     num2 = 20000
# obj1 = Child1()
# print(obj1.num1 + obj1.num2)
# obj2 = Child2()
# print(obj2.num1 + obj2.num2)



























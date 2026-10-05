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



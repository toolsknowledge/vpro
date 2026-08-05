"""
    class: collection of "variables and functions" called as "class"
    "class" is the keyword, used to "declare the class"
    "pass" is the keyword, used to declare "empty class"
    we can create "object" to the class
    in "instance" multiple copies are created
    one copy changes may not effect to other copies (instance)
"""
# Example-1
# class Test:
#     num1 = 100

# obj1 = Test()
# x = obj1.num1
# print(x)

# Example-2
# class Test:
#     num1 = 100

# obj1 = Test()
# obj1.num1 = 1000

# obj2 = Test()
# x = obj2.num1
# print(x)


# Example-3
# class Test:
#     num1 = 200
#     num2 = 100
    

# obj1 = Test()
# x = obj1.num1
# y = obj1.num2
# add = x + y
# print(f"Addition : {add}")

# Example-4
# class Test:
#     def __init__(self,param1,param2):
#         self.num1 = param1
#         self.num2 = param2

# obj1 = Test(200,100)
# x = obj1.num1
# y = obj1.num2

# multiplication = x * y
# print(f"Multiplication : {multiplication}")


# Example-5
# class Test:
#     def __init__(self):
#         pass

# obj1 = Test()
# obj1.num1 = 200
# obj1.num2 = 100

# x = obj1.num1
# y = obj1.num2
# subtraction = x - y
# print(f"Subtraction : {subtraction}")


# Example-6
# class Test:
#     def addition1(self):
#         num1 = 200
#         num2 = 100
#         res = num1 + num2
#         print(f"Addition : {res}")

#     def addition2(self,param1,param2):
#         res = param1 + param2
#         print(f"Addition : {res}")

#     def addition3(self):
#         num1 = 200
#         num2 = 100
#         res = num1 + num2
#         return res
#     def addition4(self,param1,param2):
#         res = param1 + param2
#         return res

# obj1 = Test()
# obj1.addition1()
# obj1.addition2(200,100)
# x = obj1.addition3()
# print(f"Addition : {x}")
# y = obj1.addition4(200,100)
# print(f"Addition : {y}")


# oops - inheritance (getting data from parent class to child class called as inheritance)
# 1) single level.  2) multilevel       3) multiple         4) hirarichal           5) hybrid
# Example-7

# class Parent:
#     num1 = 200

# class Child(Parent):
#     pass

# obj1 = Child()
# x = obj1.num1
# print(x)

# class Parent:
#     def test_func(self):
#         print("Hello...!")

# class Child(Parent):
#     pass

# obj = Child()
# obj.test_func()

# Example-8
# class Parent:
#     msg = "Agentic AI !!!"

# class Child(Parent):
#     msg1 = "Quantum Computing !!!"

# class Subchild(Child):
#     msg2 = "Cloud Deployment !!!"

# obj1 = Subchild()
# x = obj1.msg
# y = obj1.msg1
# z = obj1.msg2
# print(x,y,z)


# Example - 9
# class Parent1:
#     layer1 = "ML"

# class Parent2:
#     layer2 = "DL"

# class Child(Parent1,Parent2):
#     layer3 = "NLP"

# obj = Child()
# x = obj.layer1
# y = obj.layer2
# z = obj.layer3
# print(x,y,z)

# class Parent1:
#     msg = "ML"

# class Parent2:
#     msg = "DL"

# class Child(Parent2,Parent1):
#     msg = "AgenticAI"

# obj = Child()
# x = obj.msg
# print(x)


# Example-10 (Hirarichal)
# class Parent:
#     num1 = 200

# class Child1(Parent):
#     num2 = 100

# class Child2(Parent):
#     num2 = 1000

# class Child3(Parent):
#     num2 = 10000

# obj1 = Child1()
# x1 = obj1.num1
# x2 = obj1.num2
# print(x1,x2)

# obj2 = Child2()
# y1 = obj2.num1
# y2 = obj2.num2
# print(y1,y2)

# obj3 = Child3()
# z1 = obj3.num1
# z2 = obj3.num2
# print(z1,z2)


# Example-11
# class Parent:
#     num1 = 100

# class Child1(Parent):
#     num2 = 200

# class Child2(Parent):
#     num2 = 300

# class Subchild(Child2,Child1):
#     pass

# obj1 = Subchild()
# x = obj1.num1
# y = obj1.num2
# print(x,y)


# Example-12
# class Parent:
#     def __init__(self,param1):
#         self.num1 = param1

# class Child(Parent):
#     def __init__(self, param1,param2):
#         super().__init__(param1)
#         self.num2 = param2


# obj = Child(200,100)
# x = obj.num1
# y = obj.num2
# print(x,y)


# class Parent:
#     def __init__(self,num1):
#         self.num1 = num1

# class Child(Parent):
#     def __init__(self, num1,num2):
#         super().__init__(num1)
#         self.num2 = num2

# class Subchild(Child):
#     def __init__(self, num1, num2,num3):
#         super().__init__(num1, num2)
#         self.num3 = num3

# obj1 = Subchild(1000,2000,3000)
# x = obj1.num1
# y = obj1.num2
# z = obj1.num3
# print(x,y,z)


# class Parent:
#     def test_func(self):
#         print("Hello,VPro Skiils !!!")

# class Child(Parent):
#     def my_func(self):
#         super().test_func()

# obj = Child()
# obj.my_func()




# Example-13
# class Test:
#     def __init__(self,num1):
#         self.num1 = num1

#     def __init__(self, num1,num2):
#         self.num1 = num1
#         self.num2 = num2

#     def __init__(self, num1,num2,num3):
#         self.num1 = num1
#         self.num2 = num2
#         self.num3 = num3

# obj = Test(30000,2000,100)
# print(obj.num1, obj.num2, obj.num3)
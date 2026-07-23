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
class Parent:
    def __test(self):
        print("Hello")

    def wish(self):
        self.__test()

class Child(Parent):
    pass

obj = Child()
obj.wish()






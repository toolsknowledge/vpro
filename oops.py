"""
   class
   *****
        - collection of "variables and functions" called as "class"
        - "class" is the keyword, used to "declare the class"
        - "pass" is the keyword, used to create "empty class"

        - "constructors" are used to initilize the "instance members"
        -  "__init__()" called as constructor in python
        - "self" is the keyword, used to recognize the "instance members"

        Inheritance:
            getting the data from "parent class to child class" called as "inheritance"
            1) single
            2) multi level
            3) multiple
            4) hirarichal
            5) hybrid
"""
# Example-23
class Test:
    name = "JNTU"

    @classmethod
    def test_func(cls):
        cls.name = "KLU"

Test.test_func()
print(Test.name)





# Example-22
# class Test:
#     name = "JNTU"

# Test.name = "KLU"

# obj = Test()
# print(obj.name)
# print(Test.name)



# Example-21
# class Test:
#     name = "JNTU"

# obj = Test()
# obj.name = "KLU"
# print(obj.name)


# Example-20
# class Test:
#     name = "JNTU"
#     def __init__(self):
#         pass
#         #self.name = "STD1"

# obj = Test()
# print(obj.name)


# Example-19
# class Test:
#     name = "JNTU"

# obj1 = Test()
# obj2 = Test()
# print(obj1.name)
# print(obj2.name)




# Example-18
# class Parent:
#     def __init__(self):
#         self.num1 = 100

# class Child1(Parent):
#     def __init__(self):
#         super().__init__()
#         self.num1 = 1000

# class Child2(Parent):
#     def __init__(self):
#         super().__init__()
#         #self.num1 = 10000

# class Subchild(Child1,Child2):
#     def __init__(self):
#         Child1.__init__(self)
#         Child2.__init__(self)
#         #self.num1 = 100000

# obj = Subchild()
# print(obj.num1)



# Example-17 (functions)

# Example-16
# class Parent:
#     def __init__(self):
#         self.x = 1000

# class Child1(Parent):
#     def __init__(self):
#         super().__init__()
#         self.y = 2000

# class Child2(Parent):
#     def __init__(self):
#         super().__init__()
#         self.y = 20000

# obj1 = Child1()
# print(obj1.x,obj1.y)

# obj2 = Child2()
# print(obj2.x,obj2.y)



# Example-15 (Functions)


# Example-14
# class Parent1:
#     def __init__(self,num1):
#         self.num1 = num1

# class Parent2:
#     def __init__(self,num1):
#         self.num1 = num1

# class Child(Parent1,Parent2):
#     def __init__(self, param1,param2,param3):
#         Parent2.__init__(self,param2)
#         Parent1.__init__(self,param1)
#         #self.num1 = param3

# obj = Child(1,10,100)
# print(obj.num1)




# Example-13
# class Parent1:
#     def __init__(self):
#         self.num1 = 200
# class Parent2:
#     def __init__(self):
#         self.num1 = 2000
# class Child(Parent1,Parent2):
#     def __init__(self):
#         Parent1.__init__(self)
#         Parent2.__init__(self)
#         #self.num1 = 20000

# obj = Child()
# print(obj.num1)



# Example-12
# class Parent1:
#     def __init__(self):
#         self.num1 = 200

# class Parent2:
#     def __init__(self):
#         self.num2 = 100

# class Child(Parent1,Parent2):
#     def __init__(self):
#         Parent1.__init__(self)
#         Parent2.__init__(self)

# obj = Child()
# print(f"Addition : {obj.num1 + obj.num2}")



# Example-9
# class Parent:
#     def __init__(self):
#         self.num1 = 300

# class Child(Parent):
#     def __init__(self):
#         super().__init__()
#         self.num2 = 200

# class Subchild(Child):
#     def __init__(self):
#         super().__init__()
#         self.num3 = 100

# obj1 = Subchild()
# print(obj1.num1 + obj1.num2 + obj1.num3 )


# Example-8
# class Parent:
#     def test_func1(self):
#         print("Hello")
# class Child(Parent):
#     pass

# obj1 = Child()
# obj1.test_func1()



# Example-7
# class Parent:
#     def __init__(self,param1):
#         self.msg = param1

# class Child(Parent):
#     def __init__(self, param1,param2):
#         super().__init__(param1)
#         self.sub = param2

# obj1 = Child("Hello","Agentic AI")
# print(obj1.msg)
# print(obj1.sub)




# Example-6
# class Parent:
#     def __init__(self):
#         self.msg = "Hello"

# class Child(Parent):
#     def __init__(self):
#         super().__init__()
#         self.sub = "Agentic AI"

# obj1 = Child()
# print(obj1.msg)
# print(obj1.sub)

# obj2 = Parent()
# print(obj2.msg)
# print(obj2.sub)



# Example-5
# class Test:
#     # no para - no return type
#     def square1(self):
#         x = 10
#         res = x * x
#         print(f"Square : {res}")

#     # with para - no return type
#     def square2(self,num1):
#         res = num1 * num1
#         print(f"Square : {res}")

#     # no para - with return type
#     def square3(self):
#         x = 10
#         res = x * x
#         return res
    
#     # with para - with return type

# obj1 = Test()
# obj1.square1()

# obj1.square2(2)

# out = obj1.square3()
# print(out)



# Example-4
# class Test:
#     def add(self):
#         num1 = 2
#         res = num1 ** num1
#         print(res)

# obj1 = Test()
# obj1.add()




# Example-3
# class Test:
#     def __init__(self):
#         pass

# obj1 = Test()
# obj1.x = 200

# print(obj1.x)




# Example-2
# class Test:
#     def __init__(self,param1,param2):
#         self.num1 = param1
#         self.num2 = param2

# obj1 = Test(200,100)
# res = obj1.num1 + obj1.num2
# print(f"Addition : {res}")


# Example-1
# class Test:
#     def __init__(self):
#         self.num1 = 200
#         self.num2 = 100

# obj1 = Test()
# obj1.num1 = 2000

# obj2 = Test()
# print(obj2.num1)

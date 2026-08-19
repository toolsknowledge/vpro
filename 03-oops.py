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




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


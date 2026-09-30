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
class Test:
    def __init__(self):
        pass
    def __init__(self, param1):
        pass
    def __init__(self, param1,param2):
        pass

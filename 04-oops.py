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
class Test:
    def addition1(self):
        num1 = 200
        num2 = 100
        res = num1 + num2
        print(f"Addition : {res}")

    def addition2(self,param1,param2):
        res = param1 + param2
        print(f"Addition : {res}")

    def addition3(self):
        num1 = 200
        num2 = 100
        res = num1 + num2
        return res
    def addition4(self,param1,param2):
        res = param1 + param2
        return res

obj1 = Test()
obj1.addition1()
obj1.addition2(200,100)
x = obj1.addition3()
print(f"Addition : {x}")
y = obj1.addition4(200,100)
print(f"Addition : {y}")




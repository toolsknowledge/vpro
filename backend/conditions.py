# Example-1
# age = 20
# if age >= 18:
#     print("Eligible to develop Agents !!!")


# Example-2
# age = 16
# if age >= 18:
#     print("Allowed to become like a FDE !!!")
# else:
#     print("Not allowed")

# Example-3
# marks = 75
# if marks >= 90:
#     print("A")
# elif marks >= 75:
#     print("B")
# elif marks >= 60:
#     print("C")
# else:
#     print("D")

# Example-4
# x = 10
# if x > 5:
#     print("A")
# if x > 8:
#     print("B")
# if x > 15:
#     print("C")



"""
    and -- both should be "True"

    True and True --- True
    True and False -- False
    False and True -- False
    False and False -- False

    or -- atleast "one" should be True

    True or True -- True
    True or False -- True
    False or True -- True
    False or False -- False
"""

# Example-5
# age = 25
# salary = 50000
# if age >= 18 and salary >= 30000:
#     print("Eligible for Loan !!!")
# else:
#     print("Not Eligible for Loan !!!")

# Example-6
# age = 25
# is_citizen = True

# if age>=18 and is_citizen:
#     print("Eligible to apply Driving !!!")
# else:
#     print("Not Eligible !!!")


# Example-7
# age = 17
# has_permission = True
# if age>=18 or has_permission:
#     print("Allow Access !!!")
# else:
#     print("Restricted !!!")


# Example-8
# age = 25
# salary = 20000
# exp = 5

# if age >= 18 and (salary >=30000 or exp>=3):
#     print("Allow for Loan")
# else:
#     print("Not Eligible")

# Example-9
# logged_in = False
# if not logged_in:
#     print("Allow Login !!!")
# else:
#     print("Not allow to login !!!")

# Example-10
# age = 25
# has_id = True
# if age >= 18:
#     if has_id:
#         print("Entry Allowed !!!")

# Example-11
# username = "vpro"
# password = "vpro@123"

# if username == "vpro" and password == "vpro@123":
#     print("Login Success !!!")
# else:
#     print("Login Fail !!!")

"""
    False , None, 0, 0.0, "", [], (), {}, set() --- Falsy
"""
# Example-12
# username=""
# if username:
#     print("Login")
# else:
#     print("Logout !!!")

# Example-13
# items = []
# if items:
#     print("Not Empty !!!")
# else:
#     print("Empty !!!")

# Example-14
# x = 0    # False
# if x:
#     print("Hello")
# else:
#     print("Welcome")


# Example-15
# x = "0"     # True
# if x:
#     print("Hello")
# else:
#     print("Welcome")


# Example-16
# age = 20
# res = "Major" if age>=18 else "Minor"
# print(res)

# Example-17
# num1 = 200
# num2 = 100
# res = num1 if num1>num2 else num2
# print(res)


# Example-18
# num1 = 10
# num2 = 200
# num3 = 100

# res = num1 if (num1>num2) and (num1>num3) else num2 if (num2>num3) else num3
# print(res)

# Example-19
# x = 10
# try:
#     if x / 0 or x > 5:
#         print("Hello")
# except:    
#         print("Welcome")


# Example-20
# x = 10
# 5 < x < 20

#             # x > 5 and x < 20
#             # 5 < x and x < 20

# 5 < x > 20 # detailed analysis

# Example-21
# numbers = [10,20,30,40,50]
# iter() is the predefined function, used to create the iterator object
# iterator object will use next() function to access elements
# res = iter(numbers)
# print(next(res))
# print(next(res))
# print(next(res))
# print(next(res))
# print(next(res))
# print(next(res))

# Example-22
# numbers = [10,20,30]
# res = iter(numbers)
# while True:
#     try:
#         num = next(res)
#         print(num)
#     except StopIteration:
#         break
        

# Example-23
# msg = "Python"
# res = iter(msg)
# print(next(res))
# print(next(res))
# print(next(res))
# print(next(res))
# print(next(res))
# print(next(res))

# iter() --- converts iterables([],(),{}) into "iterator"
# next() -- access elements from "iterator"

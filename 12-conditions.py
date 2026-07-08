# age = 22
# if age > 18:
#     print("You are eligible to vote.")
# print("Completed.")


# age = 22
# citizen = True
# if age>18 and citizen:
#     print("You are eligible to vote.")


# username = "admin"
# password = 1234
# if username == "admin" or password == 123:
#     print("Access Granted")



# is_logged_in = False
# if not is_logged_in:
#     print("Please Login !!!")


# age = 25
# salary = 50000
# if age > 18:
#     if salary > 30000:
#         print("You are eligible for loan.")
#     else:
#         print("Low Salary")
# else:
#     print("You are not eligible for loan.")


# num = 15
# if num%2 == 0:
#     print("Even !!!")
# else:
#     print("Odd !!!")


# num = -10
# if num > 0:
#     print("Positive !!!")
# elif num < 0:
#     print("Negative !!!")
# else:
#     print("Zero !!!")

# a = 10
# b = 20
# c = 30
# if a>=b and a>=c:
#     print(a)
# elif b>=a and b>=c:
#     print(b)
# else:
#     print(c)


# name = ""
# if name:
#     print("Not Empty")
# else:
#     print("Empty") 


# nums = [10,20,30,40,50]
# if 30 in nums:
#     print("Available !!!")

# age = 19
# res = "Major" if age>18 else "Minor"
# print(res)

day = 3

match day:
    case 1:
        print("Monday")
    case 2:
        print("Tuesday")
    case 3:
        print("Wednesday")
    case 4:
        print("Thursday")
    case 5:
        print("Friday")
    case 6:
        print("Saturday")
    case 7:
        print("Sunday")
    case _:
        print("Invalid Day !!!")
    
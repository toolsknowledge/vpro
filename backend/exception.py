# exception handling
# avoid abnormal termination of application
# try, except, else, finally, raise

# Example-1
# a = 10
# b = 0

# res = a / b
# print(res)


# Example-2
# try:
#     a = 10
#     b = 0
#     res = a / b
#     print(res)
# except:
#     print("Something went wrong !!!")

# print("Program Completed !!!")


# Example - 3
# a = 10
# b = 0
# try:
#     res = a/b
#     print(res)
# except ZeroDivisionError:
#     print("can't devide with zero")

# print("Program Completed !!!")


# Example - 4
# try:
#     print(x)
# except NameError:
#     print("variable not available !!!")


# Example - 5
# try:
#     num = int("hello")
#     print(num)
# except ValueError:
#     print("unable to convert !!!")


# Example - 6
# try:
#     a = int( input("Enter A : ") )
#     b = int( input("Enter B : ") )
#     res =  a / b
#     print(res)
# except ZeroDivisionError:
#     print("user entered zero !!!")
# except ValueError:
#     print("unable to perform arthematic operation on invalid data !!!")


# Example-7
# try:
#     a = 10
#     b = 5
#     res = a / b
#     print(res)
# except:
#     print("Err !!!")
# else:
#     print("no issue with logic !!!")


# Example - 8
# try:
#     a = 10
#     b = 0
#     print(a/b)
# except ZeroDivisionError:
#     print("can't divide with zero")
# finally:
#     print("always executes, clean up operations")

# assignment
# try, multiple except, else and finally


# Example - 9
# raise (raise manual exceptions)
# age = 15
# try:
#     if age < 18:
#         raise ValueError("Age must be 18 or above")
# except ValueError as e:
#     print(e)

# ZerDivisionError
# ValueError
# NameError
# IndexError
# KeyError
# FileNotFoundError
# ImportError
# AttributeError - objects
# TypeError - 1 + "Hello"

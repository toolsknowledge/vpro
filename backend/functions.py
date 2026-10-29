"""
    function
    ********
        business logic
           (or)
        set of "statements" also called as "function"

        functions are reusable

        "def" is the keyword, used to declare/define the function
"""
# Example-1
# function definition
# no-para & no-return
# def greet():
#     print("Good Morning !!!")

# # function calling
# greet()

# Example-2
# with para - no return type
# def greet(name):
#     print(f"Welcome to {name}")

# greet("VPro")

# Example-3
# no para - with return
# def greet():
#     return "Hello"

# res = greet()
# print(res)


# Example-4
# with para - with return type
# def greet(param1):
#     return f"welcome to {param1}"

# res = greet("FDE")
# print(res)

# 1) no para - no return 
# 2) with para - no return
# 3) no para - with return
# 4) with para - with return

# Example-5
# no para - no return
# def add():
#     num1 = 200
#     num2 = 100
#     res = num1 + num2
#     print(f"Addition : {res}")

# add()

# Example-6
# def add(num1,num2):
#     res = num1 + num2
#     print(f"Addition : {res}")

# add(200,100)

# Example-7
# def add():
#     num1 = 200
#     num2 = 100
#     res = num1 + num2
#     return res

# x = add()
# print("Addition : {}".format(x))

# Example-8
# def add(param1,param2):
#     res = param1 + param2
#     return res

# x = add(200,100)
# print("Addition {}".format(x))

# Assignent - Square of a number

# Example-9
# variable-length parameters
# we will represent with "*"
# rule1: only one variable-length parameter allwed
# rule2: variable-length parameter always last
# def add(*num1):             # (10,20,30,40,50)
#     res = sum(num1)
#     print(res)

# add(10,20,30,40,50)

# Example-10
# def test_func(*param1,*param2):
    # Err : only one variable-length parameter allowed

# Example-11
# def test_func(param1,param2,*param3):
#     print(param1,param2,param3)

# test_func(10,20,30,40,50)
# test_func() # missing 2 required positional arguments
# test_func(100)  # missing 1 required positional argument: 'param2'
# test_func(100,200)  # 100 200 ()

# Example-12
# default parameters in functions
# def test_func(location="Hyd"):
#     print(location)

# # test_func()
# test_func("Vizag")

# Example-13
# def test_func(param1="Hello",param2="Welcome"):
#     print(param1,param2)

# test_func()
# test_func(100,200)
# test_func("Python","ML")

# Example-14
# param1 & param2 - positional parameters
# param3 - default parameter
# def test_func(param1,param2,param3="Hello"):
#     print(param1,param2,param3)

# test_func(10,20)
# test_func()
# test_func(10)
# test_func(10,20,30)

# Example-15
# param1 - positional
# param2 - default
# param3 - variable-length
# def test_func(param1,param2="Hello",*param3):
#     print(param1,param2,param3)

# test_func()
# test_func(100)
# test_func(10,20,30,40,50)

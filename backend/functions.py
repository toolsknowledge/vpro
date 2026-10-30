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


# Example-16
# stores the data in the form of a key & value pairs
# variable-length keyword parameter
# we will represent with **
# only one variable-length keyword parameter allowed
# it should be last in parameter list

# def test_func(**param1):
#     print(param1)

# test_func(num1=200,num2=100)


# Example-17
# def test_func(**param1,**param2):
#     pass
# Err: SyntaxError: arguments cannot follow var-keyword argument

# Example-18
# param1 - positional parameter (mandatory)
# param2 - default (Hello)
# param3 - variable-length parameter "()"
# param4 - variable-length keyword parameters "{}"
# def test_func(param1,param2="Hello",*param3,**param4):
#     print(param1, param2, param3, param4)

# test_func()     # missing 1 required positional argument: 'param1'
# test_func(10)
# test_func(10,20,30,40,50,x=10,y=20)

# Example-19
# keyword parameters in functions
# def test_func(name,course):
#     print(name, course)

# test_func(course="FDE",name="Std1")

# Example-20
# / - positional-only parameters
# we are not allowed keywords while passing the data
# def test_func(name,course,/):
#     print(name,course)

# test_func("Std1","FDE")
# test_func(course="FDE",name="Std1")
# test_func(name="Std1",course="FDE")

# Example-21
# keyword-only parameters
# we will represent with "*"
# after "*", we must pass data with keywords only (if we violate the rule, err)
# before "*" we are allowed pass either keyword or without keyword
# def test_func(name,*,age,course):
#     print(name,age,course)

# test_func("Std1",age=40,course="FDE")
# test_func("Std1",course="FDE",age=38)
# test_func(name="Std1",age=37,course="FDE")
#test_func(name="Std1",37,"AgenticAI")

# Example-22
# param 1 shud be always value
# param2 could be with or without  keyword
# param3 always with keyword
# def test_func(param1,/,param2,*,param3):
#     print(param1,param2,param3)

# use cases
# test_func("Std1",param2=40,param3="FDE")
# test_func("Std1",40,param3="FDE")
# test_func(name="Std1",param2=40,param3="FDE")
# test_func(name="Std1",40,param3="FDE")
# test_func(name="Std1",40,"FDE")

# Example-23
# lambda is the keyword, used to define the anonymous functions
# function without name called as anonymous function
# res = lambda num1: num1 + num1
# x = res(10)
# print(x)

# Example-24
# add = lambda num1,num2: num1+num2
# print(add(10,20))


# Example-25
# print( list( map(lambda num1:num1*100,[1,2,3,4,5]) ) )

# Assignment (divide each number with 2)

# Example-26
# print( tuple( filter(lambda num1:num1>=300,(100,200,300,400,500)) ) )

# Example-27
from functools import reduce
print( reduce(lambda num1,num2:num1+num2,[1,2,3,4,5]) )

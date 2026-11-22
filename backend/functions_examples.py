# function - particular business logic (or) set of statements also called as function
# "reuse" the business logic
# "def" is the keyword, used to define the functions
# "pass" is the keyword, used to create "empty" function

# Example-1
# function definition
# def greet():
#     print("Hello, welcome to functions !!!")

# function calling
# greet()
# greet()
# greet()
# greet()
# greet()


# Example-2
# def greet(param1):
#     print(f"welcome to {param1}")

# greet("AI !!!")
# greet("Quantum Computing !!!")
# greet("FDE !!!")


# Example-3
# def greet():
#     return "Welcome to AI World !!!"

# x = greet()
# print(x)

# y = greet()
# print(y)



# Example-4
# def greet(param1):
#     return f"welcome to {param1}"

# x = greet("AI")
# print(x)

# no parameter - no return type
# with parameter - no return type
# no parameter - with return type
# with parameter - with return type


# Example - 5
# no parameters - no return
# def add():
#     num1 = 200
#     num2 = 100
#     res = num1 + num2
#     print(f"Addition : {res}")

# add()


# Example - 6
# def square(num1):
#     return num1 * num1

# res = square(10)
# print(res)


# variable-length parameters
# * used to create variable-length parameter
# because of variable-length parameter, parameter converted to "tuple"
# we are allowed to pass "only one" variable-length parameter
# variable-length parameter always "last" in parameters list

# Example-7
# def test_func(*param1):
#     print(param1)

# test_func(10,20,30,40,50)
# test_func("ML","DL","NLP","GENAI","AGENTICAI")


# Example-8
# Err
# def test_func(*param1,*param2):
#     pass


# Example-9
# Err
# def test_func(param1,*param2,param3):
#     print(param1,param2,param3)

# test_func(10,20,30,40,50)


# Example-10
# default parameters
# while defining the function, we will initilize the parameters
# def test_func(param1="Hello"):
#     print(param1)

# test_func()
# test_func("Welcome")
# test_func("")
# test_func(None)


# Example-11
# def test_func(param1=200,param2=100):
#     print(param1 + param2)

# test_func()
# test_func(2000, 1000)


# Example-12
# def test_func(param1,param2="Hello",*param3):
#     print(param1, param2, param3)

# test_func()
# test_func(100)
# test_func(100,"Welcome",10,20,30,40,50)


# Example-13
# variable keyword length parameters
# because of ** param1 converted to dictionary
# we are allowed to pass only one variable keyword length parameters, always last in parameters list
# def test_func(**param1):
#     print(param1)

# test_func(name="Hello",course="Agentic AI")


# Example-14
# keyword length parameters
# def test_func(param1,param2):
#     print(param1, param2)

# test_func(param2=200, param1=100)
# test_func(param1=1, param2=2)



# function without name called as "anonymous" functions
# we will define anonymous functions with the help of "lambda" keyword
# Example - 15
# x = lambda msg:msg
# res = x("Hello")
# print(res)


# Example - 16
# add = lambda num1,num2: num1 + num2
# res = add(200,100)
# print(f"Addition : {res}")


# code for square of a number

# code for cube of a number



# Example-17
# max = lambda a,b: a if a>b else b
# res = max(200,100)
# print(res)


# find the max number among three

# find the even/odd number


# Example-18
# map() - manipulate all elements of list/tuple
# print( list( map(lambda num1: num1*100,[1,2,3,4,5]) ) )



# assignment
# [100,200,300,400,500] --> [1,2,3,4,5]

# Example-19
# filter() - used to apply conditions on list/tuple
# print( tuple( filter(lambda num1:num1>=30,(10,20,30,40,50)) ) )


# assignement
# (100,200,300,400,500) -- (100,200)

# Example-20
# from functools import reduce
# print( reduce(lambda num1,num2:num1+num2, (1,2,3,4,5)) )


# assignment (reduce)
# (1,10,100,1000,10000)


# Example-21
# from functools import reduce
# print( reduce(lambda num1,num2:num1+num2,tuple(filter(lambda num1:num1<3,tuple(map(lambda num1:num1/100,[100,200,300,400,500]))))))

# (1,2,3,4,5)
# (1,2)
# 3.0


# recursive functions
# function calling itself called as recursive function
# Example-22
# def count(n):
#     if n == 0:
#         return
#     print(n)
#     count(n-1)

# count(5)


# Example-23
# def fact(n):
#     if n == 1:
#         return 1
#     return n * fact(n-1)

# print( fact(5) )


# Example-24
# def fibo(n):
#     if n <= 1:
#         return n
#     return fibo(n-1) + fibo(n-2)

# print(fibo(6))

# Example-25
# / --> positional-only parameter separator
# def test(param1,param2,/):
#     print(param1, param2)

# test(200, 100)                            # valid
# test(param1 = 200, param2 = 100)          # invalid
# test(param2 = 2000, param1 = 1000)        # invalid


# Example-26
# def test(param1,param2,/,param3):
#     print(param1, param2, param3)

# test(10,20,30)                    # valid
# param3 --- 30 / param3=30
# test(10,20,param3=30)             # valid

# test(param1=100,param2=200, 300)      # in-valid (param1, param2)
# test(param1 = 100, param2= 200, param3=300)   # in-valid (param1, param2)


# Example-27
# Any parameter before the * can be passed positionally or by keyword, while any parameter after the * must be passed by keyword.
# * -- keyword only argument
# param1 - 10  (value)
# param2 - 20   (value)
# param3 - 30 / param3 = 30 (value / key)
# param4 - param4 = 40 (key)
# def test(param1,param2,/,param3,*,param4):      # param4 = 40 
#     print(param1, param2, param3, param4)


# test(10,20,param3=30, param4=40)


# Example - 28
# create the empty function (no impl)
# def test():
#     pass

# assignment
# defualt, variable-length (tuple), and keyword-length (dict)

# assignment
# defualt, variable-length (tuple), and keyword-length (dict), positiona-only separator(/) and keyword only argument(*)

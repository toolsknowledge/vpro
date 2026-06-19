"""
    function
    *********
        particular "business logic" called as function
              (or)
        set of statements also called as "function"

        "def" is the keyword, used to "declare" the function

        "pass" is the keyword, to represent "empty function"
"""

# no para - no return type
# def addition():
#     num1 = 200
#     num2 = 100
#     res = num1 + num2
#     print(f"Addition : {res}")

# addition()


# no para - with return type
# def addition():
#     num1 = 200
#     num2 = 100
#     res = num1 + num2
#     return res

# x = addition()
# print(x)


# with para - no return 
# def addition(num1,num2):
#     res = num1 + num2
#     print(f"Addition : {res}")

# addition(200,100)


# with para - with return 
# def addition(num1,num2):
#     res = num1 + num2
#     return res

# x = addition(200,100)
# print(f"Addition : {x}")

# no para - no return type
# no para - with return type
# with para - no return type
# with para - with return type

# square of number

# default parameters
# def test_func(num1=200,num2=100):
#     res = num1 + num2
#     print(f"Addition : {res}")

# test_func()
# test_func(2000,1000)
# test_func(2000)
# test_func(num2=1000)
# test_func(num1=1)

# normal(regular)parameters with default parameters
# def test_func(param1,param2,param3="Hello"):
#     print(param1,param2,param3)

# test_func(100,200)
# test_func(100,200,300)
# test_func(param3="Agentic AI",param2="Gen AI",param1="Python")


# variable - length arguments
# *
# param1 - tuple

# def test_func(*param1):
#     print(param1)

# test_func("Gen AI")
# test_func("Gen AI","Agentic AI")
# test_func(10,20,30,40,50)

# functions will allow only one "variable-length" argument
# def test_func(*param1,*param2):
#     pass


# def test_func(param1,param2,param3="Hello",param4="Welcome",param5=()):
#     print(param1,param2,param3,param4,param5)

# test_func(100,200) #100 200 Hello Welcome ()
# test_func(param3=300,param1=100,param2=200,param4=400) #100 200 300 400 ()
# test_func(param1=1,param2=2,param3=3,param4=4,param5=(5,6,7,8,9,10))
# test_func(param1=1,param2=2,param3=3,param4=4,param5=(5,6,7,8,9,10))

# keyword arguments
# **
# key-value pairs (dict)

# def test_func(**param1):
#     print(param1)

# test_func(name="VPro",sub="Gen AI")

# def test_func(param1,param2="Hello",*param3,**param4):
#     print(param1,param2,param3,param4)

# test_func(100)
# test_func(100,200,300,400,500,num1=600,num2=700)

# normal
# default
# variable-length
# keyword-legth arguments

# def test_func(*subjects):
#     for sub in subjects:
#         print(sub,end=" ")

# test_func("Gen AI","Agentic AI","RAG","MCP","MCP Client")


# lambda - anonymous functions
# x = lambda num1: num1 * num1
# print(x(10))

# x = lambda num1,num2: num1+num2
# print(x(200,100))

"""
    1. 2. 3. 4. 5
         x100.                  map()
    100 200 300 400 500
    --------------------------------------
    1000 2000 3000 4000 5000
        > 3000                  filter()
    4000 5000
    --------------------------------------
    1 2 3 4 5
                                reduce()
    15

    1.20min - Sat & Sun. 09:00PM - 10.15PM
    Sugg : LLMops, RAG, MCP , 

"""
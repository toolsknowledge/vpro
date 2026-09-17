"""
    function - business logic
                 (or)
               set of "statements" also called as "function"
    
    functions are used to "reuse" the business logic

    "def" is the predefined keyword, used to declare the functions

    "pass" is the keyword,used to declare empty function
"""

# function definition
# no parameters - no return 
# def addition():
#     num1 = 200
#     num2 = 100
#     res = num1 + num2
#     print(f"Addition : {res}")

# function calling
# addition()


# function definition
# with parameters - no return
# def addition(num1,num2):
#     res = num1 + num2
#     print(f"Addition : {res}")

# function calling
# addition(200,100)

# no parameters with return type
# def addition():
#     num1 = 200
#     num2 = 100
#     res = num1 + num2
#     return res

# x = addition()
# print(f"Addition : {x}")

# with parameters - with return
# def addition(num1,num2):
#     res = num1 + num2
#     return res

# x = addition(200,100)
# print(f"Addition : {x}")


"""
    variable-length parameter
    *************************
    * --> parameter turned to "tuple"

    we are able to create only "one" variable-length parameter
"""

# def my_func(*param1):
#     print(type(param1))         # <class 'tuple'>
#     print(param1)

# my_func(10,20,30,40,50)      # (10, 20, 30, 40, 50)

# Err - unable to pass more than one variable-length parameter
# def my_func(*param1,*param2):
#     pass

# param1,param2 - positional parameters
# param3 - variable-length parameter
# Note : variable-length parameter must be last (in combination : posi + variable-length)

# def my_func(param1,param2,*param3):
#     print(param1, param2, param3)

# my_func(10,20,30,40,50)



# keyword parameters
# def my_func(param1,param2):
#     print(param1, param2)

# my_func(10,20)
# my_func(param2="Hello",param1="welcome")


# default parameters in functions
# def my_func(num1=200,num2=100):
#     print(num1,num2)

# my_func()
# my_func(2000,1000)
# my_func(num2=10000)
# my_func(10000)
# my_func(None)

# keyword-length parameters
# ** --> param converted to dictionary
# always last 
# def my_func(**param1):
#     print(type(param1))
#     print(param1)

# my_func(name="VPro",course="GenAI")


# we are unable to pass, more than one keyword-length parameters
# def my_func(**param1,**param2):
#     pass

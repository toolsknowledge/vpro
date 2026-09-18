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


# keyword-only parameters
# def my_func(name, *, age, city):
#     print(name, age, city)

# my_func("Samba",age=40,city="Hyderabad")
# my_func(name="Samba",age=40,city="Hyderabad")
# my_func("Samba",city="Hyderabad",age=40)
# my_func("Samba",40,"Hyderabad")       # Err


# positional-only parameters ("/")
# before /, we are allowed to pass data directly
# def my_func(name,age,/):
#     print(name, age)

# my_func("Samba",40)
# my_func(name="Samba",age=40)        # Err

# name - positional parameter (normal parameter)
# age - default parameter
# skills - variable-length parameter (tuple)
# city - default

# details - keyword-length parameters (dictionary)
# def my_func(name,age=20,*skills,city="Hyderabad",**details):
#     print(name,age,skills,city,details)

# my_func("Samba",40,"Java","AI",city="Hyd",m1="Python",m2="GenAI",m3="AgenticAI")
    

# square = lambda num1: num1 * num1
# res = square(2)
# print(res)


# add = lambda num1,num2 : num1 + num2
# res = add(200,100)
# print(res)


# check = lambda num1: "Even" if num1%2 == 0 else "Odd"
# res = check(10)
# print(res)

 
# large = lambda num1,num2,num3: num1 if (num1>num2) and (num1>num3) else num2 if num2>num3 else num3
# res = large(10,20,30)
# print(res)


# map() - manipulate all list/tuple elements
# res = list( map(lambda num1: num1*10,[1,2,3,4,5]) )
# print(res)


# res = list( map(lambda name:name.upper(),["sudheer","ravi","rinkal"]) )
# print(res)



# filter()
# used to apply conditions on lists/tuples
# res = list( filter(lambda num1:num1%2 == 0, [1,2,3,4,5]) )
# print(res)

# reduce()
# used to find the sum of list/tuple elements
# from functools import reduce
# res = reduce(lambda num1,num2:num1+num2,[10,20,30,40,50])
# print(res)

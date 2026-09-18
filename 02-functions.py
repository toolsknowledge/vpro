"""
    business logic
        (or)
    set of statements also called as function

    functions are used to "reuse" the business logic

    "def" is the keyword, used to declare the functions

    "pass" is the keyword, used to create empty function   
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


# no parameters - with return
# def addition():
#     num1 = 200
#     num2 = 100
#     res = num1 + num2
#     return res


# x = addition()
# print(f"Addition : {x}")


# with parameters - no return 
# def addition(num1,num2):
#     res = num1 + num2
#     print(f"Addition : {res}")

# addition(200,100)

# with parameters - with return
# def addition(num1,num2):
#     res = num1 + num2
#     return res

# x = addition(200,100)
# print(f"Addition : {x}")


# def my_func(*param1):
#     print(param1)

# my_func(100,200,300,400,500)


# def my_func(*param1,*param2):



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













# function - particular "business logic" called as "function"
# set of statements also called as "function"
# functions are used to reuse the "business logic"
# "def" is the keyword, used to declare the function
# "pass" is the keyword, used to declare empty functions

# no parameters - no return
# def addition():
#     num1 = 200
#     num2 = 100
#     res = num1 + num2
#     print(f"Addition : {res}")

# addition()

# no parameters - with return 
# def addition():
#     num1 = 200
#     num2 = 100
#     res = num1 + num2
#     return res

# x = addition()
# print(f"Addition : {x}")

# with parameters - no return type
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


# variable - length parameters
# * used to create variable - length parameter
# parameter behaves like "tuple"
# each function, will allow only "one" variable-length parameter
# variable-length parameter, must be "last" in parameters list

# def addition(*num):
#     print(sum(num))

# addition(10)
# addition(10,20,30)
# addition(10,20,30,40,50)


# def test(param1,param2,*param3):
#     print(param1,param2,param3)

# test(200,100,10,20,30,40,50)


# default parameters in functions
# def test(num1=200,num2=100):
#     print(num1, num2)

# test()
# test(2000,1000)
# test(num2=1000)
# test(num2=None)
# test(num1=None)

# formal parameters,default parameters and variable length parameter
# def test(param1,param2,param3=200,param4="Hello",*param5):
#     print(param1, param2, param3, param4, param5)

# test()
# test(1000)
# test(1,2)
# test(1,2,3,4,5,6,7,8,9,10)
# test(param1=1000,param2=2000,param3=3000,param4=4000)


# keyword - length parameters
# because of **, param1 converted to dictionary
# stores the data in the form of a key & value pairs
# def test(**param1):
#     print(param1["empid"])
#     print(param1["empname"])
#     print(param1["empsal"])

# test(name="Emp1")
# test(empid=101,empname="emp1",empsal=10000)

# positional-parameters, default-parameters, variable-length parameters and keyword-length parameters
# def test(emp_id,name,department="IT",*skills,**details):
#     print(f"Employee ID : {emp_id}")
#     print(f"Employee Name : {name}")
#     print(f"Department : {department}")
#     print(f"Skills : {skills}")
#     print(f"Other Details are : {details}")

# test(101,"Emp1","CSE","Python","ML","DL","GenAI","AgenticAI",address="Hyderabad",state="Telangana")


# lambda - create anonymous functions
# square = lambda num1: num1 * num1
# res = square(10)
# print(f"Square : {res}")

# cube = lambda num1: num1 ** 3
# res = cube(10)
# print(f"Cube : {res}")

# addition = lambda num1,num2:num1 + num2
# res = addition(200,100)
# print(f"Addition : {res}")

# check = lambda num1: "Even" if num1%2 == 0 else "Odd"
# res = check(9)
# print(f"Result : {res}")

# maximum = lambda num1,num2: num1 if num1>num2 else num2
# res = maximum(100,200)
# print(f"Result : {res}")


# list1 = [1,2,3,4,5]
# res = list( map(lambda num1:num1*100,list1) )
# print(res)

# list1 = [100,200,300,400,500]
# res = list( filter(lambda num1:num1>=300,list1) )
# print(res)

# from functools import reduce
# list1 = [1,2,3,4,5]
# res = reduce(lambda num1,num2:num1+num2,list1)
# print(f"Sum....{res}")

# from functools import reduce
# list1 = [1,2,3,4,5]
# res1 = list( map(lambda num1:num1*10,list1) )       # [10,20,30,40,50]
# res2 = list( filter(lambda num1:num1<=30,res1) )    # [10,20,30]
# sum = reduce(lambda num1,num2:num1+num2,res2)       # [60]
# print(sum)


# Faq - 1
# def test():
#     return 10,20,30

# t1 = test()
# print(t1,type(t1))

# Faq - 2
# def add(num1,num2):
#     res = num1 + num2
#     print(res)

# numbers = [200,100]
# add(*numbers)


# Faq - 3
# def add(num1,num2):
#     res = num1 + num2
#     print(res)

# d1 = {"num2":100,"num1":200}
# add(**d1)

# Faq - 4
# Recurssive functions
# function calling itself
# def print_numbers(n):
#     if n == 6:
#         return

#     print(n)
#     print_numbers(n+1)

# print_numbers(1)

# def factorial(n):
#     if n == 1:
#         return 1

#     return n * factorial(n-1)

# print(factorial(5))     # 5 * factorial(4)
                        # 5 * 4 * factorial(3)
                        # 5 * 4 * 3 * factorial(2)
                        # 5 * 4 * 3 * 2 * factorial(2)
                        # 5 * 4 * 3 * 2 * 1
                        # 120


# Faq - 5
def reverse(str):       
    if len(str) == 0:
        return ""
    return reverse(str[1:]) + str[0]

print( reverse("Hello") )           # reverse("ello") + H
                                    # reverse("llo") + e + H
                                    # reverse("lo") + l + e + H
                                    # revesr("o") + l + l + e + H
                                    # reverse("") + o + l + l + e + H
                                    # "" + o + l + l + e + H
                                    # olleH











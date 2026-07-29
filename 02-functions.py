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
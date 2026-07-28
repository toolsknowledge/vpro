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
"""
    function - particular "business logic"
            (or)
    set of "statements" also called as "function"

    "functions" are used to reuse the "business logic"

    "def" is the keyword, used to "declare" the functions
"""

# declare the function
# def add1():
#     x,y = 1000,2000
#     res = x + y
#     print(f"Addition : {res}")

# call the function
# add1()
# add1()
# add1()
# add1()
# add1()


# def add2():
#     num1 = num2 = 2000
#     res = num1 + num2
#     return res

# x = add2()
# print(f"Addition : {x}")


# def add3(param1,param2):
#     res = param1 + param2
#     print(f"Addition : {res}")

# add3(200,100)



# no para - no return
# no para - with return
# with para - no return
# with para - with return

# def add4(num1,num2):
#     res = num1 + num2
#     return res

# x = add4(200,100)
# print(f"Addition : {x}")



# keyword parameters
# def db_func(username,password):
#     res = "Login Success" if username == "vpro" and password == "vpro@123" else "Login Fail"
#     return res

# x = db_func(password="vpro@123",username="vpro")
# print(x)



# default parameters in functions
# def test(param1=200,param2=100):
#     res = param1 + param2
#     print(res)


# test()
# test(2000,1000)
# test(20000)
# test(param2=10000)

# formal parameters with default parameters
# Note : in combination of "fommal(positional) and default", always "default paramreters" must be "last"
# def test(param1,param2,param3="Hello",param4="Welcome"):
#     print(param1,param2, param3, param4)

# test()
# test(100)
# test(1,2)
# test(1,2,3,4)
# test(param2=200,param4=100,param1=1000,param3=2000)
# test(None,None)

# variable-length parameter (param1 - tuple)
# def test(*param1):
#     print(param1)

# test()
# test(10,20,30,40,50)
# test("Python","ML","DL","NLP","GenAI","AgenticAI")

# only one variable-length parameter allowed
# def test(*param1,*param2):


# param1 & param2 - formal parameters
# param3 & param4 - default parameters
# param5 - variable-length parameter
# def test(param1,param2,param3="Hello",param4="Welcome",*param5):
#     print(param1,param2,param3,param4,param5)

# test()
# test(1)
# test(1,2)
# test(1,2,3,4,5,6,7,8,9,10)


# def test(param1,*param2,param3="Hello"):
#     print(param1,param2,param3)

# test()
# test(10)
# test(10,20,30)
# test(10,20,30,40,50,60,70)


# valid
# def test(param1,param2="Hello"):
#     pass

# valid
# def test(param1,*param2):
#     pass

# invalid
# def test(param1="Hello",param2):
#     pass

# invalid
# def test(*param1,param2):
#     pass

# valid
# def test(param1,*param2,param3="Hello"):
#     pass

# invalid
# def test(*param1,param2="Hello",param3):
#     pass

# default parameters
# def addition(num1=200,num2=100):
#     res = num1 + num2
#     print(res)

# addition()
# addition(2000,1000)
# addition(2000)
# addition(num1=10000)
# addition(num2=20000)
# addition(None)


# param1 & param2 - formal parameters
# param3 & param4 - default parameters
# Note : default parameters must be last 
# def test(param1,param2,param3="Hello",param4="Welcome"):
#     print(param1, param2, param3, param4)

# test()
# test(100)
# test(100,200)
# test(param4=400,param1=100,param3=300,param2=200)

# variable-length parameter
# because of "*", param1 converted to tuple
# def test(*param1):
#     print(param1)

# test(10,20,30,40,50)
# test()
# test("Python","ML","DL","NLP","GenAI","AgenticAI")
# test(None,"Hello",100)

# Note : only one variable-length parameter allowed
# def test(*param1,*param2):

# param1 - formal (non-default)
# param2 - default parameter
# param3 - variable-length parameter

# def test(param1,param2="Hello",*param3):
#     print(param1,param2,param3)

# test()
# test(100)
# test(100,200,300,400,500)


# def test(param1,*param2,param3="Hello"):
#     pass


# Note : default parameter, must be followed by non-default parameter
# Err
# def test(param1,*param2,param3="Hello",param4):
#     pass


# keyword-length parameter
# because of **, param1 converted to dictionary
# we are able to pass only one dict parameter

# def test(**param1):
#     print(param1)

# test(name="Hello",course="GenAI")


# def test(param1,param2=100,*param3,**param4):
#     print(param1,param2,param3,param4)

# test()
# test(10)
# test(1,2,3,4,5,6,name="Good Morn...!")


# Note1: default order must be "secondary" with non-default
# Note2: only one tuple parameter
# Note3: only one dictionary parameter
# Note4: dictionary parameter always last
# def test(param1,*param2,param3="Hello",**param4):
#     print(param1,param2,param3,param4)

# test()
# test(None)


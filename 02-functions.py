# function definition

# no parameters - no return
# def square():
#     num1 = 2
#     res = num1 * num1
#     print(res)

# function calling
# square()


# no parameter - with return
# def square():
#     num1 = 10
#     res = num1 * num1
#     return res

# x = square()
# print(x)

# with parameters - no return
# def square(num1):
#     res = num1 * num1
#     print(res)

# square(100)

# with parameters - with return
# def square(num1):
#     res = num1 * num1
#     return res

# x = square(10)
# print(x)


# in definition itself, initilize parameters called ad default parameters in functions
# def test(num1=200,num2=100):
#     print(num1, num2)

# test()
# test(1,2)
# test(num2=1000)
# test(2000)

# param1 & param2 - positional parameters
# param3 - default paramerer
# def test(param1,param2,param3="Hello"):
#     print(param1, param2, param3)

# test()
# test(100)
# test(1,2)
# test(1,2,3)


# def test(*param1):
#     print(param1)

# test(10,20,30,40,50)
# test()
# test("Python","ML","DL","NLP","GENAI","AGENTICAI")

# Note : functions wont allows more than one variable-length parameter
# def test(*param1,*param2):
#     pass

# param1 - positional
# param2 - default
# param3 - variable-length parameters

# def test(param1,param2="Hello",*param3):
#     print(param1, param2, param3)

# test()
# test(100)
# test(1,2,3,4,5)

# keyword-length parameters
# last
# only one keyword-length parameter allowed
# param1 - dictionary
# key-value pairs

# def test(**param1):
#     print(param1)

# test()
# test(name="VPro")
# test(name="VPro",course="AgenticAI")


# param1 - positional
# param2 - default
# param3 - variable-length
# param4 - keyword-length parameter
# def test(param1,param2=100,*param3,**param4):
#     print(param1, param2, param3, param4)

# test()
# test(1)
# test(1,2,3,4,5,num1=100,num2=200)
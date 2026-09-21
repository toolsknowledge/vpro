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


# def outer():
#     def inner():
#         print("Hello")
#     inner()

# outer()


# Closure
# def outer():
#     name = "VPro"

#     def inner():
#         print(name)
#     inner()

# outer()


# def outer():
#     course = "AgenticAI"

#     def inner():
#         print(course)

#     return inner        # outer function return inner function definition

# x = outer()
# x()


# def outer():
#     count = 0

#     def inner():
#         nonlocal count
#         count += 1
#         return count

#     return inner

# x = outer()
# print(x())
# print(x())
# print(x())


# def print_numbers(num):
#     if num == 0:
#         return

#     print_numbers(num-1)
#     print(num)

# print_numbers(5)


# def factorial(num):
#     if num == 1:
#         return 1

#     return num * factorial(num-1)

# factorial(5)


# res = lambda num1:num1 * num1
# print(res(10))


# add = lambda num1,num2: num1 + num2
# print(add(200,100))


# print( list( map(lambda num1:num1*100, [10,20,30,40,50]) ) )

# print( list( filter(lambda num1:num1>=3,[1,2,3,4,5]) ) )

from functools import reduce
print( reduce(lambda num1,num2:num1+num2,[10,20,30,40,50]) )














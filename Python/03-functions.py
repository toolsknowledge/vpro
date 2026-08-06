# Example-1
# no parameters - no return type
# def addition():
#     num1 = 200
#     num2 = 100
#     res = num1 + num2
#     print(f"Addition : {res}")

# addition()


# Example-2
# no parameters - with return type
# def addition():
#     num1 = 200
#     num2 = 100
#     res = num1 + num2
#     return res

# x = addition()
# print(f"Addition : {x}")

# Example-3
# with parameters - no return type
# def addition(num1,num2):
#     res = num1 + num2
#     print(f"Addition : {res}")

# addition(200,100)

# Example-4
# with parameters - with return type
# def addition(num1,num2):
#     res = num1 + num2
#     return res

# x = addition(200,100)
# print(f"Addition : {x}")


# Example-5
# Default Parameters (while declaraing the functions, we are initilizing parameters)
# def test(name="VPro"):
#     print(name)

# test()
# test("VPro Skills Edu Tech")


# Example-6
# def test(num1 = 100,num2 = 200):
#     print(num1, num2)

# test()
# test(1000,2000)
# test(num2=2000)
# test(num1=1000)
# test(num1=10000)

# Example-7 (normal + default) Note : default parameters always last
# def test(param1,param2,param3="Hello",param4="Welcome"):
#     print(param1,param2,param3,param4)

# test() # Err :missing 2 required positional arguments
# test(100) # Err: missing 1 required positional argument
# test(200,100)
# test(400,300,200,100)
# test(400,300,200)
# test(400,300,param4=100)

# Example-8
# Global Variable
# x = 100

# def test():
#     # Local Variable
#     x = 200
#     print(x)

# test()

# Example-9 (Faq : local variable must be initilized "NameError")
# def test():
#     x
#     print(x)

# test()

# Example-10 (Global Variable also must be initilized "NameError")
# x
# def test():
#     print(x)
# test()

# Example-11
# x = 100
# def test():
#    global x 
#    x = x+1
#    print(x)

# print(x)
# test()
# print(x)

# Example-12
# def test(*param1):
#     print(param1)

# test(10,20,30,40,50)


# Example-13
# def test(*param1):
#     print(param1)
#     print(type(param1))
#     print(len(param1))
#     x = param1[0]   # x --> HTML
#     y = tuple(x)    #["H","T","M","L"]
#     z = y[::-1]
#     print(z)


# test("HTML","CSS","JS","ML","DL","NLP","GENAI","AGENTICAI")

# Example-14 (Err: only one variable length parameter allowed)
# def test(*param1,*param2):
#     pass


# Example-15
# order
# 1) positional parameters. 2) default parameters. 3) variable-length parameters 

# def test(param1="100",param2,*param3):
#     pass

# def test(*param1,param2,param3="Hello"):
#     print("Hello")

# test(10,20)

# def test(param1="Hello",param2):
#     pass

# def test(param1,param2=200,param3=100,*param4):
#     print(param1,param2,param3,param4)

# test(10)
# test(10,20,30,40,50)
# test(param1=10,param3=20)


# Example-16
# keyword-length parameters
# def test(param1,param2="Hello",*param3,**param4):
#     print(param1,param2,param3,param4)

# test(10)
# test(10,20,30,40,name="Hello")


# Example-17
# functions without name called as "lambda functions"
# "lambda" is the keyword, used to declare the lambda functions

# add = lambda num1,num2: num1+num2
# res = add(200,100)
# print(res)

# Square of a number
# Cube of a number

# Example-18
# even = lambda num1: num1%2 == 0
# res = even(10)
# print(res)

# res1 = even(9)
# print(res1)

# Example-19
# large = lambda num1,num2: num1 if num1>num2 else num2
# print(large(200,100))
# print(large(10,20))

# find the largest among three

# Example-20
# map() - used to manipulate all elements from lists and tuples

# res = list(map(lambda num1:num1*10,[1,2,3,4,5]))
# print(res)

# res = list(map(lambda num1:num1*100,(1,2,3,4,5)))
# print(res)


# res = tuple(map(lambda num1:num1*1000,[1,2,3,4,5]))
# print(res)

# res = tuple(map(lambda num1:num1*1000,(1,2,3,4,5)))
# print(res)

# Example-21
# filter() - used to apply conditions
# res = list(filter(lambda num1: num1%2==0,[1,2,3,4,5]))
# print(res)

# Example-22
# reduce() - sum of all elements
# from functools import reduce
# res = reduce(lambda num1,num2:num1+num2,[1,2,3,4,5])
# print(res)

# Example-23 (Recurssive Functions)
# def print_numbers(num):
#     if num > 5:
#         return
#     print(num)
#     print_numbers(num+1)

# print_numbers(1)

# Example-24
# def factorial(num):
#     if num == 1:
#         return 1
#     return num * factorial(num-1)   # 5 * 4 * 3 * 2 * 1    

# print(factorial(5))


# Example-25
def sum(num):
    if num == 1:
        return 1
    
    return num + sum(num-1)     # 5 + 4 + 3 + 2 + 1

print(sum(5))



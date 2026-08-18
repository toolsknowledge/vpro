# function - business logic (or) set of statements
# reuse the business logic
# "def" is the keyword,used to declare the function
# "pass" is the keyword, used to declare "empty function"

# Example-1
# def test():
#     print("welcome to functions !!!")

# test()


# Example-2 no parameters - no return type
# def addition():
#     num1 = 200
#     num2 = 100
#     res = num1 + num2
#     print(f"Addition : {res}")

# addition()

# Example-3 no parameters - with return type
# def addition():
#     num1 = 200
#     num2 = 100
#     res = num1 + num2
#     return res

# x = addition()
# print(f"Addition : {x}")


# Example-4 (with parameters and no return type)
# def addition(num1,num2):
#     res = num1 + num2
#     print(f"Addition : {res}")

# addition(200,100)


# Example-5 (with para - with return type)
# def addition(num1,num2):
#     res = num1 + num2
#     return res

# x = addition(1,100)
# print(f"Addition : {x}")


# Example-6 (keyword parameters)
# def db_func(username,password):
#     res = "Login Success" if username == "vpro" and password == "vpro@123" else "Login Fail"
#     return res

# res = db_func(password="vpro@123",username="vpro")
# print(res)


# Example-7 (variable length parameter) (*)
# def test(*param1):
#     print( sum(param1) )

# # test(100,200)
# test(1,2,3)

# Example-8 (invalid)
# def test(*param1,*param2):

# Example-9 (positional parameters and variable-length parameter) (variable-length parameter always last)
# def test(param1,param2,*param3):
#     print(param1, param2, param3)

# test(1,2,3,4,5)
# test("Python","ML","DL","NLP","GenAI","AgenticAI")


# Example-10
# def variableLengthParam(*param1):
#     return sum(param1)

# x = variableLengthParam(1,2,3)
# print(f"Sum of values: {x}")


# Example-11 (Default Parameters)
# def test(param1="Hello"):
#     print(param1)

# test()
# test("Welcome")
# test(None)


# Example-12
# pos & defualt -- last (default)
# default & variable-length -- last(variable-length)
# pos, default and variable-length -- last (variable length)
# def test(p1,p2,p3=100,p4=200,*p5):
#     print(p1,p2,p3,p4,p5)

# test()  # missing 2 required positional arguments
# test(10,50)
# test(10,100,1000,10000,2,20,200,2000,20000)

# Example-13
# def test(p1,p2=100,p3=()):
#     print(p1,p2,type(p3))
# test(p1=10,p3="100")

# Example-14 (keyword-length parameter)
# def test(**param1):
#     print(param1)

# test(key1=100,key2=200,key3=300)


# Example-15
# def test(p1,p2=100,*p3,**p4):
#     print(p1,p2,p3,p4)

# test()
# test(10)
# test(10,1000,1,2,3,4,5,key1=100,key2=200)

# lambda - function without name
# x = lambda num1:num1*num1
# res = x(10)
# print(res)


# add = lambda x,y:x+y
# print(add(1,2))

# res = lambda num1:"Even" if num1%2==0 else "Odd"
# print(res(10))
# print(res(9))


# res = lambda num1,num2,num3:(num1 if ((num1>num2) and (num1>num3)) else num2 if (num2>num3) else num3)
# print(res(10,20,30))
# print(res(100,20,30))

# Curring
# Closure
# outer = lambda num1:lambda num2:lambda num3:num1+num2+num3
# middle = outer(10)
# inner = middle(20)
# res = inner(30)
# print(res)


# Example-16
# print( list(map(lambda num1:num1*100,[1,2,3,4,5])) )
# print( list( map(lambda x,y:x+y,(1,2,3,4,5),(10,11,12,13,14)) ) )
# print( tuple(map(lambda num1,num2:num1-num2,[1,2],[1,2,3,4,5])) )
# print( list( map(int,"10 20 30 40 50".split()) ) )
# res = map(lambda x:x**x,[1,2,3,4,5]) # Iterator
# x = list(res)
# print(x)
# y = list(res)
# print(y)

# print( tuple( filter(lambda num1:num1>=3,(1,2,3,4,5)) ) )
# print( list( map(lambda num1:num1*num1, filter(lambda num1:num1%2 == 0,[1,2,3,4,5,6]) ) ) )
# print( list( map(None,[1,2,3,4,5]) ) )

# res = map(lambda res: list(map(lambda y: y * 100,res)),[[1, 2], [3, 4], [5, 6]])
# print(list(res))

# from functools import reduce
# print(reduce(lambda num1,num2:num1+num2,[1,2,3,4,5]))


# Example-17
# def countdown(n):
#     if n == 0:
#         return
#     print(n)
#     countdown(n-1)

# countdown(5)

# def factorial(n):
#     if n==0:
#         return 1
#     return n * factorial(n-1)

# print(factorial(5))



# Faq1
# def test_func(item,items=[]): # [10]
#     items.append(item)        # [10,20]
#     return items

# print( test_func(10) )
# print( test_func(20) )

# def test_func(item,items=None):
#     if items is None:
#         items = []
#     items.append(item)
#     return items
# print(test_func(10))
# print(test_func(20))

# list1 = [1,2,3]
# list2 = [1,2,3]
# print(list1 is list2)
# print(list1 == list2)


# list1 = [1,2,3]
# list2 = list1
# print(list1 is list2)
# print(list1 == list2)

# num1 = 257
# num2 = 257
# print(num1 == num2)
# print(num1 is num2)


# True - 1. False - 0 * "Boolean" is the child datatype of "Integer"
# print(True + True + False)
# print(isinstance(True,int))
# print(isinstance(False,int))
# print(isinstance(True,bool))

# print(True == 1)
# print(True is 1)    # False


# list1 = [1,2,3]
# list2 = list1
# list2.append(4)
# print(list1)

# print( tuple(range(5)) )        #[0,1,2,3,4]
# print( list(range(1,10)) )
# print( list(range(0,5,2)) )       # 0 2 4
# print( list(range(10,0,-1)))
# print( list(range(5,0,-2)) )

# Compression
print( [x*x for x in range(5) if x%2 == 0] )





"""
    functions
    *********
        particular "business logic" called as "function"
                (or)
        set of "statements" also called as function

        functions are used to "reuse" the business logic

        "def" is the keyword, used to "define" the function

        "pass" is the keyword, used to define the "empty function"
"""

# Example-1
# Function Defintion
# No Parameters - No Return
# def addition():
#     num1 = 200
#     num2 = 100
#     res = num1 + num2
#     print(f"Addition : {res}")

# Function Calling
# addition()


# Example-2
# No Parameters - with Return Type
# def addition():
#     num1 = 200
#     num2 = 100
#     res = num1 + num2
#     return res

# x = addition()
# print(f"Addition : {x}")

# Example-3
# With Parameters - No Return Type
# def addition(num1,num2):
#     res = num1 + num2
#     print(f"Addition : {res}")

# addition(200,100)


# Example-4
# with parameters and with return type
# def addition(num1,num2):
#     res = num1 + num2
#     return res

# x = addition(200,100)
# print(f"Addition : {x}")


"""
    variable-length parameter
    *************************
        * used to create the variable-length parameter
        because of variable-length parameter, param behaves like tuple
        Note : we are allowed to pass only one variable-length parameter per function
"""
# Example-5
# def test_func(*param1):
#     print(param1)

# test_func(10,20,30,40,50)


# Example-6
# def test_func(*param1,*param2):
#     pass

# Example-7
# param1 & param2 - positional parameters (mandatory)
# param3 - variable-length parameter
# def test_func(param1,param2,*param3):
#     print(param1, param2, param3)

# test_func()           # Error
# test_func(200)        # Error
# test_func(200,100)    # 200 100 ()
# test_func(200,100,300,400,500)


# Example-8
# variable-lenght parameter always last in parameters-list
# def test_func(*param1,param2,param3):
#     pass
# test_func(10,20,30,40,50)


"""
    initilizing parameters during function defintion itself called as
    default parameters in functions
"""
# Example-9
# def test_func(param1="Hello",param2="VPro"):
#     print(param1, param2)

# test_func()
# test_func("FDE")
# test_func(param2="VPro EduTech")
# test_func(None)


# Example-10
# param1 & param2 - positional parameters (mandatory)
# param3 & param4 - default parameters
# def test_func(param1,param2,param3=100,param4=200):
#     print(param1,param2,param3,param4)

# test_func()
# test_func(1)
# test_func(1,2)

# Example-11
# in positional and default combination, default must be last in parameters list
# def test_func(param1=100,param2):
#     print(param1,param2)


# Example-12
# param1 - positional
# param2 - default
# param3 - variable-length parameter
# Rule 1: in positional and default -- default must be 2nd priority
# Rule 2: in position and variable-length - variable-length must be 2nd priority
# def test_func(param1,param2=100,*param3):
#     print(param1,param2,param3)
# test_func(10,20,30,40,50)

# Example-13
# def test_func(param1,*param2,param3=100):
#     print(param1, param2, param3)

# test_func(10,20,30,40,50)


"""
    keyword-length parameters
    *************************
        ** - used to create "keyword-length" parameter
        param behaves like a "dictionary" (key & value pairs)
        keyword-length parameters always "last"
        only "one" keyword-length parameter allowed
"""
# Example-14
# def test_func(**param1):
#     print(param1)

# test_func(name="Samba",cmp="VPro")
    

# Example-15
# def test_func(**param1,**param2):
#     pass


# Example-16
# def test_func(param1,param2=100,*param3,**param4):
#     print(param1, param2, param3, param4)
# test_func()
# test_func(10)


# Example-17
# def test_func(num1,num2):
#     print(num1,num2)

# test_func(200,100)
# test_func(num1=2,num2=1)              # keyword-only parameters
# test_func(num2=2000,num1=1000)
# test_func(num1=10000,20000)


# Example-18
# * - keyword-only
# after * compulsary keyword-only
# def test_func(num1,*,num2,num3):
#     print(num1,num2,num3)

# test_func(1,num2=2,num3=3)
# test_func(num1=1,num2=2,num3=3)
# test_func(1,2,3)


# Example-18 (positional-only parameters) /
# def test(name,age,/):
#     print(name,age)

# test("emp1",20)     # emp1 20
# test(name="emp1",age=20) # Err


# Example-19
# def test(param1,param2,/,param3,param4):
#     print(param1, param2, param3, param4)

# param1 & param2 - positional
# param3 & param4 - positional or keyword
# test(10,20, 30,40)
# test(100,200, param3=300,param4=400)
# test(param1=1000,param2=2000,3000,4000)

"""
    lambda
    ******
        function without name called as anonymous functions
        we will declare anonymous functions with "lambda" keyword
"""
# Example-20
# pow = lambda num1:num1**num1
# res = pow(10)
# print(res)

# Example-21
# add = lambda num1,num2 : num1 + num2
# res = add(2,1)
# print(res)

# Example-22
# check = lambda num: "Even" if num%2 == 0 else "Odd"
# res = check(9)
# print(res)


# Example-23
# large = lambda num1,num2: num1 if num1>num2 else num2
# res = large(20,10)
# print(res)


# Example-24
# large = lambda num1,num2,num3: num1 if (num1>num2) and (num1>num3) else num2 if num2>num3 else num3
# print(large(10,20,30))
# print(large(-10,20,1))


# Example-25
# list1 = [10,50,20,40,30]
# res = sorted(list1)         # immutable
# print(res)
# print(list1)

# Example-26
# list1 = [23,15,42,31,18]        # [3, 5, 2, 1, 8]
# res = sorted(list1, key=lambda num:num%10)
# print(res)


"""
    map() - manipulate all list/tuple elements
"""
# Example-27
# print( list( map(lambda num1:num1*100,[1,2,3,4,5]) ) )


"""
    filter() - used to apply conditions on list/tuple elements
"""
# Example-28
# print( tuple( filter(lambda num1:num1>=30,(10,20,30,40,50)) ) )



"""
    reduce() - used to find the sum of list/tuple elements
"""
# Example-29
# from functools import reduce
# print( reduce(lambda num1,num2:num1+num2,[1,2,3,4,5]) )


"""
    recursion
        function calling itself called as recursion
"""
# Example-30
# def display(n):
#     if n>5:
#         return
#     print(n)
#     display(n+1)

# display(1)


# Example-31
# def factorial(n):
#     if n == 0 or n == 1:
#         return 1
#     return n * factorial(n-1)           # 5 x factorial(4)
#                                         # 5 x 4 x factorial(3)
#                                         # 5 x 4 x 3 x factorial(2)
#                                         # 5 x 4 x 3 x 2 x factorial(1)
#                                         # 5 x 4 x 3 x 2 x 1
#                                         # 120
# print(factorial(5))



# Example-32
# def fibonacci(n):
#     if n <= 1:
#         return n
#     return fibonacci(n-1) + fibonacci(n-2)

# for i in range(7):      # [0,1,2,3,4,5,6]
#     print(fibonacci(i),end=" ")


"""
    closure
    *******
        inner function, remember and access outer function data, even thoe outer function execution completed
        called as closure
"""
# Example-33
# def outer():
#     count = 10
#     def inner():
#         print(count)
#     return inner

# x = outer()
# x()



"""
    generator functions
    *******************
        generator functions will return value by value insted of all values at a time
        generator functions internally uses "yield" keyword
        "yield" keyword, will return value by value
"""
# Example-34
# def test():
#     yield 10
#     yield 20
#     yield 30

# itr = test()
# print(next(itr))
# print(next(itr))
# print(next(itr))


# Example-35
# def outer():
#     x = 10
   
#     def inner():
#         x = 20
#         print(x)        # 20
#     inner()
   
#     print(x)            # 10
# outer()


# def outer():
#     x = 10
   
#     def inner():
#         nonlocal x
#         x = 20
#         print(x)        # 20
#     inner()
   
#     print(x)            # 20
# outer()



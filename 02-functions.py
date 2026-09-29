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


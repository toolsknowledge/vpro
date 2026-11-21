# function - particular business logic (or) set of statements also called as function
# "reuse" the business logic
# "def" is the keyword, used to define the functions
# "pass" is the keyword, used to create "empty" function

# Example-1
# function definition
# def greet():
#     print("Hello, welcome to functions !!!")

# function calling
# greet()
# greet()
# greet()
# greet()
# greet()


# Example-2
# def greet(param1):
#     print(f"welcome to {param1}")

# greet("AI !!!")
# greet("Quantum Computing !!!")
# greet("FDE !!!")


# Example-3
# def greet():
#     return "Welcome to AI World !!!"

# x = greet()
# print(x)

# y = greet()
# print(y)



# Example-4
# def greet(param1):
#     return f"welcome to {param1}"

# x = greet("AI")
# print(x)

# no parameter - no return type
# with parameter - no return type
# no parameter - with return type
# with parameter - with return type


# Example - 5
# no parameters - no return
# def add():
#     num1 = 200
#     num2 = 100
#     res = num1 + num2
#     print(f"Addition : {res}")

# add()


# Example - 6
# def square(num1):
#     return num1 * num1

# res = square(10)
# print(res)


# variable-length parameters
# * used to create variable-length parameter
# because of variable-length parameter, parameter converted to "tuple"
# we are allowed to pass "only one" variable-length parameter
# variable-length parameter always "last" in parameters list

# Example-7
# def test_func(*param1):
#     print(param1)

# test_func(10,20,30,40,50)
# test_func("ML","DL","NLP","GENAI","AGENTICAI")


# Example-8
# Err
# def test_func(*param1,*param2):
#     pass


# Example-9
# Err
# def test_func(param1,*param2,param3):
#     print(param1,param2,param3)

# test_func(10,20,30,40,50)


# Example-10
# default parameters
# while defining the function, we will initilize the parameters
# def test_func(param1="Hello"):
#     print(param1)

# test_func()
# test_func("Welcome")
# test_func("")
# test_func(None)


# Example-11
# def test_func(param1=200,param2=100):
#     print(param1 + param2)

# test_func()
# test_func(2000, 1000)


# Example-12
# def test_func(param1,param2="Hello",*param3):
#     print(param1, param2, param3)

# test_func()
# test_func(100)
# test_func(100,"Welcome",10,20,30,40,50)


# Example-13
# variable keyword length parameters
# because of ** param1 converted to dictionary
# we are allowed to pass only one variable keyword length parameters, always last in parameters list
# def test_func(**param1):
#     print(param1)

# test_func(name="Hello",course="Agentic AI")


# Example-14
# keyword length parameters
# def test_func(param1,param2):
#     print(param1, param2)

# test_func(param2=200, param1=100)
# test_func(param1=1, param2=2)


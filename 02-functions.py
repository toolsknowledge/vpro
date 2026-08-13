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






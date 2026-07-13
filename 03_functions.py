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




















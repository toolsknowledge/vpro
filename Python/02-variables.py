# x = 100

# def test():
#     global x
#     x = x + 10
#     print(x)
    
# print(x)
# test()
# print(x)



# name = "Gen AI"

# def test():
#     name = "Agentic AI"
#     print(name)

# test()
# print(name)




# x = 100

# def test():
#     # x = 10      # Local Variable
#     x = x + 1
#     print(x)

# test()




# Global Variable
# x = 100

# def test():
#     print(x)

# test()




# x = 100
# del x
# print(x)



# == (compares values) is - memory location
# list1 = [10,20,30]
# list2 = [10,20,30]
# print(list1 == list2)
# print(list1 is list2)



# list1 = []
# list2 = []
# list2.append(100)
# print(list1)
# print(list2)



# list1 = list2 = []
# list1.append(100)
# print(list1)
# print(list2)


# a = b = c = 100
# b = 200
# print(a)
# print(b)
# print(c)


# a = 10
# b = 20

# a, b = b, a
# print(a)
# print(b)




# a = 10
# b = 10

# a, b = 10, 10
# print(a)
# print(b)

# a = b = 10
# print(a)
# print(b)

# None - empty / no value
# salary = None
# print(type(salary))

# salary = 100000
# print(salary)


# Set - never allows duplicates, unordered, hetrogeneous, no indexes, "Search", Hashable, {} / set() constructor
# s1 = {10,20,30,10,20,30}
# print(s1)

# s2 = set({10,20,10})
# print(s2)

# s3 = set([10,10])
# print(s3)

# s4 = set((10,20,10,20,30,20))
# print(s4)

# s5 = {}
# s6 = set()
# print(type(s5))
# print(type(s6))

# s7 = {"Hello","Hello",10,10,20}
# print(s7)




# dictionary - key & value pairs, keys are "immutable",values are "mutable", {} / dict() (constructor)
# d1 = {
#     "name" : "VPro",
#     "sub" : "AgenticAI",
#     "version" : 1
# }
# print(d1)
# print(d1["name"])
# print(d1.keys())
# print(d1.values())
# print(d1.items())
# print(type(d1))

# d1 = {}
# print(type(d1))

# d2 = {
#     (10,20) : "Hello"
# }
# print(d2)



# Tuple - collection of values, hetrogeneous, Ordered, index-0, (), immutable
# tuple1 = (10,20,30,40,50)
# print(tuple1)
# print(type(tuple1))
# print(tuple1[0:2])
    # [10,20,30]
    # [20,30,40]

# tuple2 = (10,20,30,40,50)
# tuple2[0] = 1000




# List - collection of values, hetrogeneous, Ordered, index-0, [], mutable
# list1 = ["VPro",2,True,100.0]
# print(list1)
# print(type(list1))

# list2 = [10,50,30,40,20]
# print(list2[0],list2[-5])
# print(list2[2],list2[-3])
# print(list2[0:3])   #[10, 20, 30]
# print(list2[:2])    #[10, 20]
# print(list2[2:])    #[30, 40, 50]
# print(list2[-4:-1]) #[20, 30, 40]
# print(list2[-3:])   #[30, 40, 50]
# print(len(list2))
# print(max(list2))
# print(min(list2))
# print(sum(list2))
# print(sum(list2) / len(list2))
# list2.sort()
# print(list2)

# list2 = [10,20,30,40,50]
# list2[0] = 100
# print(list2)








# integer - numbers (int,float)
# num1 = 200
# num2 = 100
# addition = num1 + num2
# print(f"Result :{addition}")

# num1 = 0x123ABC
# print(num1)

# num2 = 0o123
# print(num2)

# num3 = 0b101010
# print(num3)


# print(10 % 3)   # Reminder : 1
# print(2 ** 3)   # power : 8
# print(10 // 2)  # Floor Division : 5
# print(10 / 2)   # Division : 5.0
# print(20 / 3)

# num1 = 123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789
# print(num1)


# num1 = 10.123
# print(num1)
# print(type(num1))


# num1 = 99.12345
# print(round(num1,2))
# print(round(num1,3))
# print(round(num1,6))
# print(round(num1,0))

# print(f"{num1:.2f}")
# print(f"{num1:.4f}")

# print(format(num1,".2f"))
# print(format(num1,".4f"))

# num1 = 0.1
# num2 = 0.2
# num3 = num1 + num2  
# print(num3) # 0.30000000000000004

# == (comapres values)
# print(10 == 10)
# print(0.1+0.2 == 0.3)
# print(0.1+0.2 == 0.30000000000000004)

# Boolean
# True - 1 & False - 0

# flag = True
# flag1 = False
# print(flag)
# print(flag1)
# print(type(flag))

# print(True + True)
# print(True + 1)
# print(True + False + 1 + 0 + True)
# print(False / True)
# print(True / False) #ZeroDivisionError: division by zero
# print("1" + True) # TypeError: can only concatenate str (not "bool") to str

# Falsy Values : False, None, 0, 0.0, "", [], {}, (), set()
# Truthy Values : True,       1, 100.1, "Hello", [10], {"num1":10}, (10,)


# num1 = 25.99
# print(int(num1))

# num2 = "25"
# print(int(num2))

# print(int(True))
# print(int(False))

# num1 = 25
# print(float(num1))

# num2 = "25.0"
# print(float(num2))

# x = 10
# print(x.bit_length())


# string - collection of characters
# ""(double quotes), '' (single quotes) , """ """(triple quotes)
# declare paragraphs we will use """ """(triple quotes)

# wish = "Welcome"
# print(wish)


# name = "VPro"
# print("Welcome to ",name)


# name = "VPro"
# msg = "Welcome " + name
# print(msg)

# course = 'AgenticAI'
# print(course)

# msg = """
#     welcome to VPro
#     and we will cover GenAI & AgenticAI
# """
# print(msg)

# course = "AgenticAI"
# version = 1.0
# print(f"Welcome to {course} and version is {version}")

# name = "Rahul"
# age = 21
# print("Student name is {} and age is {}".format(name,age))

# print("GenAI\nAgenticAI")
# print("GenAI\tAgenticAI")
# print('welcome to "AgenticAI"')

# print("LLM "," GENAI",sep='→')
# print("C:\\OneDrive\\Desktop")

# name = "VPro"
# print(type(name))










  
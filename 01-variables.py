# dictionary
# key - value pairs
# keys are immutable and values are mutable
# {}

# d1 = {
#     "name" : "Hello",
#     "age" : 40
# }
# print(d1)
# print(d1.keys())
# print(d1.values())
# print(d1.items())
# print(d1["name"])
# d1["name"] = "Welcome"
# d1.pop("name")
# print(d1)

# tuple
# collection of hetrogeneous elements
# ()
# positive index starts from "0" and negative index starts from "-1"
# immutable

# t1 = (10,20,30,40,50)
# print(t1)
# print(type(t1))
# print(t1[0],t1[-5])
# len
# sum
# max
# min
# avg
# sort (ascending / decending)

# t1 = (100,200,300,400,500)
# t1[4] = 5000

# import sys
# list1 = [10,20,30]
# t1 = (10,20,30)
# print(sys.getsizeof(list1))
# print(sys.getsizeof(t1))


# List
# collection of "hetrogeneous" elements
# []
# positive index starts from "0" and negative index starts from "-1"
# mutable (we can modify)

# list1 = [10,20,30,40,50]
# print(list1[2],list1[-3])
# list1[0] = 1000
# print(list1)
# print(len(list1))
# print(sum(list1))
# print(max(list1))
# print(min(list1))
# print(sum(list1) / len(list1))
# list1.sort()
# print(list1)
# list1.sort(reverse=True)
# print(list1)
# print( 40 in list1 )
# print( 400 in list1 )
# print( 4000 not in list1 )
# list1.remove(40)
# print(list1)





# flag = True
# flag1 = False
# print(flag, type(flag))
# print(flag1, type(flag1))
# print(isinstance(flag,int))
# print(isinstance(flag1,int))
# print(int(True))
# print(int(False))
# print(isinstance("Hello",str))
# print(isinstance(10,int))






# print("ML","DL","NLP","Gen AI","AgenticAI",sep="---->")


# x = "Hello"
# y = "Agentic AI"
# print(x,end = " | ")
# print(y,end = "!")



# sub = "Python"
# print(sub)

# sub1 = 'Deep Learning !!!'
# print(sub1)

# sub2 = """
#         in upcoming companies looking for
#         Machine Learning with Quantum Computing !!!
# """
# print(sub2)

# msg = "Hello"
# print(msg[0],msg[-5])
# print(msg[4],msg[-1])
# print(msg[::-1])
# print(msg[::-2])
# print(msg[::-3])
# print(msg[0:2])
# print(msg[-3:])

# print("Hello \n Python")
# print("Hello \t Python")
# print("Hello how \"are\" you")
# path = r"C:\Users\Admin"
# print(path)

# print("Python " * 20)
# print("Hello" + " Python")
# print("10" + "20")
# print( int("10") + int("20") )
# print("Hello " + 20) # Err


# name = "VPro"
# sub = "Agentic AI"
# print(f"{name} Started {sub}")

# sub1 = "Quantum Computing"
# version = 1.0
# print(f"{name} will start {sub1} with {version} version soon !!!")


# name = "Samba"
# age = 40
# print("my name is {} and age is {}".format(name,age))
# print("my name is {1} and age is {0}".format(age,name))












# import keyword
# print(keyword.kwlist)

# num1 = 100
# print(num1)

# num2 = -100
# print(num2)

# num3 = 0
# print(num3)

# # num4 = 0100

# num5 = 10_000
# print(num5)

# print(True + True)
# print(1 + True + False)

# num6 = 123456789123456789123456789123456789123456789123456789123456789
# print(num6)

# num7 = 0x123ABC
# print(num7)

# num8 = 0o123
# print(num8)

# num9 = 0b101010
# print(num9)

# num10 = "10"
# print(type(num10))
# x = int(num10)
# print(type(x))

# num11 = "10.5" 
# y = float(num11)
# z = int(y)
# print(z)

# print(int(True))
# print(int(False))

# print(float(True))
# print(float(False))

# # print(int("Hello"))
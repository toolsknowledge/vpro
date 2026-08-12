# Varibables are used to "store" the data
# Ex. Integer(Ex. 100), String (Ex. "Hello") Ex. Boolean (True / False) Ex. list Ex.[]  , tuple Ex.()....... 
# Rules to declare Variables
# Rule 1. declaration must contain a-z,A-Z,0-9,$ and _
# Rule 2. declaration never starts with "digits"
# Rule 3. never use "predefined keywords" as "variables declaration"

# String
# collection of "characters"
# 1) "" (double quotes).  2) '' (single quotes).  3) """ """ (tripple quotes)
# """ """ (tripple quotes), used to declare the paragraphs

# wish = "Hello"
# print(wish)

# msg = 'Python'
# print(msg[0],msg[-6])
# print(msg[0:2])
# print(msg[:2])
# print(msg[4:])
# print(msg[-2:])
# print(msg[::-1])

# content = """
#         1) Python
#         2) ML (10+)
#         3) DL (Image Processing)
#         4) NLP (ChatBot)
#         5) Gen AI (Tools)
#         6) Agentic AI
#         7) Cloud Integrations
# """
# print(content)

# x = "Hello"   #(immutable)
# x[0] = "h"
# print("h"+x[1:])

# msg = "Gen AI"
# MSG = "AGENTIC AI"
# Msg = "Quantum"
# print(msg,MSG,Msg)

# name = "emp1"
# age = 40
# print(f"Employee Name is {name} and Age is {age}")
# print("Employee Age  {} and his name is {}".format(age,name))

# Integer
# num1 = 200
# num2 = 100
# add = num1 + num2
# print(f"Addition is {add}")
# sub = num1 - num2
# print("Subtraction : {}".format(sub))

# int
# numbers (positive numbers / negative numbers / zeros)
# immutable (we can't modify)
# unlimited size

# Example-1
# num1 = 100
# num2 = -100
# num3 = 0
# print(num1)
# print(num2)
# print(num3)
# print(type(num1))

# Example-2
# num1 = 123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789
# print(num1)

# num2 = 2 ** 1000
# print(num2)

# Example_3
# num1 = 1_23_456_78
# print(num1)

# x = 1_00
# y = 2_00
# z = x + y
# print(z)

# num2 = _100  # Ex. Err


# Example-4
# num1 = 0B11001
# print(num1)

# num2 = 0O31
# print(num2)

# num3 = 0X19
# print(num3)

# Example-5
# num1 = 25
# print(bin(num1))
# print(oct(num1))
# print(hex(num1))


# Example-6 (ASCII)
# print(ord('A'))
# print(ord('a'))
# print(chr(65))
# print(chr(97))


# Example-7 (True - 1 / False - 0)
# In Python "Booleans are Integers"

# print(True + True)
# print(True + False + 1)
# print(True / False)   # Err.ZeroDivisionError
# print(False / True)
# print("1" + True)   # Err
# print("1" + 1) # Err


# Example-9
# == (compare values)
# is (objects)
# print(1 == True)
# print(0 == False)

# print(1 is True)
# print(0 is False)


# Example-10
# print(abs(-100))
# print(2 ** 2)
# Floor Division (rounded)
# print( 10 // 3 )    
# Division
# print( 10 / 3 )
# Reminder (perventages)
# print(10%3 ) 

# Example - 11
# & (and) both should be true
# | (or) either one should be true
# ^ (xor) both should be different

# print( True and True )
# print( True | False )
# print( False | True )
# print( True ^ False )
# print( True ^ True )

# Example-12
# num1 = 0.1         
# num2 = 0.2
# num3 = num1 + num2      # 0.30000000000000004
# print(num3)

# print(0.1 + 0.2 == 0.3 )


# boolean
# True - 1 & False - 0
# in "True" T must be "capital" and in False "F" must be "capital"
# boolean is the "child data" type for integer
# flag = True
# print(f"Boolean Value : {flag}")

# flag1 = False
# print(f"Boolean Value : {flag1}")

# print(type(flag))

# res = "GenAI" if flag else "Agentic AI"
# print(res)

# res1 = "GenAI" if flag1 else "Agentic AI"
# print(res1)

# age = 20
# citizen = True
# if age>18 and citizen:
#     print("Eligible for Vote !!!")
# else:
#     print("Not Eligible")


# list
# colloection of elements
# hetrogeneous  [1,"Hello",1.2,True]
# ordered
# positive / negative
# mutable
# [] / list() constructor
# allows duplicates

# list1 = [10,20,30,40,50]
# list1.append(60)
# list2 = [70,80]
# list1.extend(list2)
# list1.append(10)
        # [10,20,30,40,50,60,70,80,10]
# list1.remove(10)
# list1.pop()
# print(list1)

# list1 = [10,20,30,40,50]
# print(list1[0])
# print(list1[-5])
# print(list1[0:2])     # 0 & 1 included.  and 2 excluded
# print(list1[:3])
# print(list1[3:])
# print(list1[::-1])
# print(list1[::-2])
# print(list1[::-3])
# print(list1[::2])
# print(list1[::3])

# list1 = [10,20,30,40,50]
# list1[0] = 1_000 # mutable      
# print(list1)

# tuple
# colloection of elements
# hetrogeneous  (1,"Hello",1.2,True)
# ordered
# positive / negative
# immutable
# () / tuple() constructor
# allows duplicates

# import sys
# list1 = [10,20,30,40,50]
# print(sys.getsizeof(list1))

# tuple1 = (10,20,30,40,50)
# print(sys.getsizeof(tuple1))


# tuple1 = 10,20,30,40,50
# print(type(tuple1))
# print(tuple1[0:2])
# print(tuple1[::2])
# print(tuple1[::3])
# print(tuple1[-4:-2])
# print(tuple1[::-1])



# dictionary
# key & value pairs
# {} / dict()
# keys are immutable and values are mutable
# key and value separated by using ":"

# d1 = {
#     "key1" : "GenAI",
#     "key2" : "AgenticAI",
#     "key3" : "RAG"
# }
# print(d1)
# print(d1.keys())
# print(d1.values())
# print(d1.items())
# print(type(d1))

# d2 = {
#     (10,20) : (10,20)
# }
# print(d2)

# d1 = {
#     "key1" : "GenAI",
#     "key2" : "AgenticAI",
#     "key3" : "RAG"
# }
# for x in d1.keys():
#     print(x)

# for y in d1.values():
#     print(y)

# for k,v in d1.items():
#     print(k,v)


# Set
# never allows duplicates
# {} / set()
# unordered

# s1 = {10,20,10,20,30}  
# print(s1)

# s2 = {}
# print(type(s2))

# s3 = set()
# print(type(s3))


# list1 = [10,20,10,30,20]
# s4 = set(list1)
# print(s4)

# tuple1 = (10,20,10)
# s5 = set(tuple1)
# print(s5)


# None
# None Representing "No-Value"
# x = None
# print(x)
# print(type(x))

# print(x == 0)
# print(x == False)
# print(x == "")

# if x == None:
#     x = "Project Assigned"

# print(x)


# String        Integer         Boolean                List             Tuple           Dict    Set     None

# num1 = num2 = num3 = 1000
# print(num1, num2, num3)

# x,y,z = 1000,2000,3000
# print(x,y,z)

# a = 1000
# b = 2000
# print(f"Before Swap a : {a} and b:{b}")
# b,a = a,b
# print(f"After Swap a : {a} and b:{b}")

# a,b,c = 10
# print(a,b,c)


# print( list(range(5)) )
# print( tuple(range(10)) )
# print( list(range(1,5)) )
# print( list(range(1,10,2) ))
# print( tuple(range(10,0,-1)) )

# a = 10
# b = 20
# res = a if a>b else b
# print(res)

a = 10
b = 15
c = 20
res = a if a>b and a>c else b if b>c else c
print(res)

























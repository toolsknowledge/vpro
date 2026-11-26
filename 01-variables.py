# variables are used to store the data
# Ex. String, Integer, Boolean,....
# Ex. msg = "VPro"
# python supports multiple datatypes
# 1) String (str)
# 2) Integer (int)
# 3) float
# 4) boolean (bool)
# 5) list
# 6) tuple
# 7) dictionary
# 8) Set
# 9) None

# String
# collection of "characters" called as "String"
# 1) "" (double quotes)     2) single quotes ('')       3) """ """ (triple quotes)
# to create multiline string (paragraphs) we will use """ """ (triple quotes)

# Example-1
# msg = "VPro"
# print(msg)


# Example-2
# sub = "FDE"
# msg = f"Welcome to {sub}"
# print(msg)


# Example-3
# sub = "Agentic AI"
# version = 1.0
# msg = f"{sub} cureent version {version}" 
# print(msg)

# Example - 4
# x = 200
# y = 100
# statement = "num1 value is {} and num2 value is {}".format(x,y)
# print(statement)


# Example-5
# frontend = "ReactJS"
# backend = "FastAPI"
# database = "Postgress"
# AI = "agentic ai"
# cloud = "Multi Cloud"
# fde = f"""
#         Frontend : {frontend}
#         Backend : {backend}
#         DataBase : {database}
#         AI FullStack : {AI}
#         Deployement : {cloud}
# """
# print(fde)


# Example-6
# str = "Hello"
# print(str[0])
# print(str[-5])
# print(str[4])
# print(str[-4])
# print(str[::2]) # skip 1 character
# print(str[::3]) # skip 2 characters
# print(str[::-1])    # reverse
# print(str[::-2])    # skip 1 character in reverse
# print(str[::-3])    # skip 2 characters in reverse



# Example-7
# str = "Welcome"
# print(str[0:3])
# print(str[0:4])
# print(str[:2])      #0:2
# print(str[3:])
# print(str[:1+1])    # 0:2
# print(str[1:4])
# print(str[-2:])
# print(str[-4:])
# print(str[-7:-5])

# Example - 8 (FAQ)
# strings are immutable
# str = "Hello"
# str[0] = "h"

# Example-9
# str = "Hello"   # ello
# res = "h" + str[1:]
# print(res)

# integer
# whole numbers
# num1 = 200
# num2 = 100
# add = num1 + num2
# print(f"Addition : {add}")
# sub
# mul
# div

# x = 2_0_0_0
# y = 1_0_0_0
# z = x + y
# print(z)


# float (accurate) (python & js)
# fractional numbers
# x = 0.1
# y = 0.2
# z = x + y
# print(z)        # 0.3
                # 0.30000000000000004


# Boolean
# True & False (T is the Catital) (F is the Capital)
# Boolean Datatype is the Child DataType of Integer 
# True - 1 & False - 0
# flag = True
# flag1 = False
# res = "AgenticAI" if flag else "Gen AI"
# print(res)

# res1 = "AgenticAI" if flag1 else "Gen AI"
# print(res1)

# print(1 + True)
# print(True + True)
# print(True + 1 + False + True)
# print(True / False)
# print(False / True)

# type() - used to know the datatype
# print( type("Hello") )      # <class 'str'>
# print( type(100) )          # <class 'int'>
# print( type(10.1) )         # <class 'float'>
# print( type(True) )         # <class 'bool'>
# print( isinstance(1,int) )
# print( isinstance(True,int) )

# sub1 = "gen ai"
# sub2 = "agentic ai"
# print(sub1,sub2,sep=" ➜ ")

# x = 200
# y = 100
# print(x,end=" & ")
# print(y)


# num1 = 200
# num2 = 100

# res = num1 if num1 > num2 else num2
# print(res)

# num1 = 300
# num2 = 2000
# num3 = 30000

# res = num1 if ((num1 > num2) and (num1>num3)) else num2 if num2>num3 else num3
# print(res)
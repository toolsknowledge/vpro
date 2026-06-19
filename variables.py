"""
    variables
    *********
        variables are used to "store the data"
        Ex.
            number
            string
            boolean
            list
            ---
            ---
            ---
            ---
        DataType Representing "Type of data"
        Python supports following "DataTypes"
        1) string
        2) int
        3) boolean
        4) list
        5) tuple
        6) dictionary
        7) set
        8) None 

        string
        ******
            collection of characters called as string
            we will represent string in 3 ways
            1) "" (double quotes)
            2) '' (single quotes)
            3) """""" (triple quotes)
        
            (triple quotes) used to define paragraphs
"""

# str = "Python"
# # P - 0 and -6
# # n - 5 and -1
# print(str[2]) # t
# print(str[-4]) # t
# print(str[0:2]) # 0included and 2 excluded
# print(str[:3]) # 0 included and 3 excluded
# print(str[2:]) # index 2 to last


# course = """
#     here, we will cover
#     1) Python
#     2) ML
#     3) DL
#     ---
#     ---
#     ---
# """
# print(course)


# str - immutable (we can't modify)
# x = "Hello"
# x[0] = "h" #TypeError: 'str' object does not support item assignment

# str = "Hello"
# print("h"+str[1:])     # hello

# str = "VPro"
# str1 = str * 3
# print(str1)

# str = "Hello"
# print(str[::-1])

# str = "Hello"
# print(str[::-2])
# print(str[::-3])

# str = "Hello"
# print(str[-1:-3])

# count() - count the repeated characters
# str = "aaaa"
# print(str.count("a"))
# print(str.count("aa"))

# str = "banana"
# print( str.replace("a","A") )
# print( str.replace("a","A",1))

# print(["a"] * 3)

# integer
# 1) int 2) float 3) complex

# float() - int - float
# num = 10
# print(float(num))

# float - int
# num = 10.6
# print(int(num))

# str = "100"
# print(int(str))
# print(float(str))

# c = 5 + 4j
# print(c.real)
# print(c.imag)
# print(type(c))

# price = 100.12345
# print(price)
# print(type(price))


# num1 = 2000
# num2 = 1000
# add = num1 + num2
# print(f"Addition : {add}")
# sub = num1 - num2
# print(f"Subtraction : {sub}")
# num3 = -100
# print(num3)
# print(type(num1))

# div 5
# print( 10 / 2 ) 

# floor 3
# print( 10 // 3 )

# modulus 1
# print( 10 % 3 )

# print( 2 ** 5 )

# print(0.1 + 0.2)  #0.30000000000000004
# print(0.1+0.2 == 0.3) # False

# import math
# print(math.isclose(0.1+0.2, 0.3))

# boolean (True - 1)  & (False - 0)
# flag = True
# flag1 = False
# print(flag)
# print(flag1)
# print(True + True)
# print(1 + True)
# print(1 + True + 0 + False)
# print(True / False)
# print(False / True)

# flag = True
# res = "Gen AI" if flag else "Agentic AI"
# print(res)

# flag1 = False
# res1 = "Gen AI" if flag1 else "Agentic AI"
# print(res1)

# list
# Ordered
# Mutable
# []
# index starts from 0
# hetrogeneous elements

# list1 = [10,20,30,40,50]
# print(list1[0])
# print(list1[-5])
# print(list1[0:3])
# print(list1[-3:-1])
# print(list1[3:])
# print(list1[:2])
# print(list1[::-1])
# print(list1[::-2])
# print(list1[::-3])

# import sys
# list2 = [10,"Hello",True,10.1,None]
# list2[0] = 1000
# print(sys.getsizeof(list2))
# print(list2)

# tuple
# ordered
# immutable
# hetrogeneous
# ()
# index also starts from "0"
# tuples, ocupies less memory compared to lists
# tuple operations are faster compared to lists (hashtable)

# import sys
# list1 = [10,20,30,40,50]
# tuple1 = (10,20,30,40,50)
# print(sys.getsizeof(list1))
# print(sys.getsizeof(tuple1))


# tuple1 = (10,20,30,40,50)
# tuple1[2] = 3000        #TypeError: 'tuple' object does not support item assignment


# tuple1 = (10,20,30,40,50)
# list() - tuple to list
# list1 = list(tuple1)
# list1[0] = 1000
# tuple() - list to tuple
# tuple2 = tuple(list1)
# print(tuple2)
# print(id(tuple1))
# print(id(list1))

# dictionary
# key - value pairs
# keys are "immutable" (we can't modify)
# values are "mutable" (we can modify)
# {}

# d1 = {
#     "name" : "vpro",
#     "sub" : "Agentic AI"
# }
# print(d1)
# print(d1.keys())
# print(d1.values())
# print(d1.items())

# d1 = {
#     "name" : "Agentic"
# }
# d1["name"] = "Agentic AI"
# d1["f_sub"] = "Quantum Computing"
# print(d1)

# d1 = {}
# d1["key1"] = 100
# d1["key2"] = 200
# d1["key3"] = 300
# d1["key1"] = 1000
# d1.pop("key2")
# d1.popitem()
# print(d1)

# Set
# never allows duplicates
# {}

# s1 = {10,20,30,10,20,30}
# print(s1)

# s2 = set([10,20,30,10,20,30])
# print(s2)

# s3 = set((10,20,10,20))
# print(s3)

# None (empty / no value)
# x = None
# print(x)
# print(type(x))

# %s - string
# %d - number
# %f  - float
# name = "VPro"
# print("I am the founder of %s" % name)

# sub = "Agentic AI"
# ver = 2
# print("Current Trending Sub is %s and Respective Version is %d" % (sub,ver))

# fever = 97.5
# print("Fever = %f" %fever)
# print("Fever = %.2f" %fever)

# name = "VPro"
# year = 2025
# print("name is {} and established in {}".format(name,year))
# print("name is {1} and established in {0}".format(year,name))

# name = "VPro"
# year = 2025
# print(f"Name is {name} and established in {year}")

# num1 = 100
# num2 = 0x123ABC
# print(num2)

# num3 = 0o123
# print(num3)

# num4 = 0b1010
# print(num4)

from rich import print
print("[red]Hello[/red]")
print("[bold green]VPro[/bold green]")
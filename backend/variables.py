# str = "VPro"
# print(str)

# str1 = 'Hello, FDE !!!'
# print(str1)

# str3 = """
#     Frontend : React
#     Backend : Python
#     Agents : Single Agent & Multi Agent
#     Cloud Services : Bed Rock / Azure
# """
# print(str3)

# msg1 = "VPro"
# msg2 = f"Hello, {msg1}"
# print(msg2)

# x = "Hello"
# y = "Welcome"
# print(x,y,sep=" | ")
# print(x,y,sep="\n")

# fend = "React"
# bend = "Python"
# database = "Postgress"
# cloud = "Azure"
# msg = "frontend: {} backend: {} database: {} and cloud {}".format(fend,bend,database,cloud)
# print(msg)

# num1 = 200
# num2 = 100
# add = num1 + num2
# print(f"Addition : {add}")

# sub = num1 - num2
# print(f"Subtraction: {sub}")

# power = num1 ** num2
# print(f"power {power}")

# num1 = 1_00
# num2 = 2_00
# print(num1+num2)

# num1 = 123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789
# print(num1)

# x = 0.1
# y = 0.2
# z = x + y       # 0.3
# print(z)        # 0.30000000000000004 (python is more accurate while adding the fractions)

# flag = True
# flag1 = False
# print(flag)
# print(flag1)

# True - 1 and False - 0
# print(True + True)
# print(True + 1 + False + 0)
# print(True / False)     # ZeroDivisionError: division by zero
# print(False / True)   

# flag = True
# flag1 = False
# res = "Hello" if flag else "Welcome"      
# print(res)

# res1 = "Hello" if flag1 else "Welcome"      
# print(res1)


# list
# collection of "hetrogeneous" elements called as list
# [] / list() constructor
# it supports both "positive" indexes and "negative" indexes
# mutable

# list1 = [10,20,30,40,50]    
# print(list1[0])
# print(list1[-3])
# print(list1[-1])
# print(list1[3])
# print(list1[::2])       # [10,30,50] skip - single element
# print(list1[::3])       # [10,40]    skip - two elements
# print(list1[::-1])      # [50,40,30,20,10]
# print(list1[::-2])      # [50,30,10]
# print(list1[::-3])      # [50,20]
# print(list1[0:3])         # 0,1,2 - included and 3 onwards excluded
# print(list1[:4])        # 0:4 # 0,1,2,3 - included
# print(list1[2:])          # index 2 - end
# print(list1[:1+1+1])    # 0:3 - 0,1,2
# print(list1[-3:])
# print(list1[-3:-1])       # -3,-2 - included, -1 excluded

# print(len(list1))
# print(max(list1))
# print(min(list1))
# print(sum(list1))
# print(sum(list1) / len(list1))


# list2 = [10,20,30,40,50]
# list2[0] = 1000
# list2[4] = 5000
# print(list2)

# list2.append(60)
# print(list2)

# list2.insert(1,15)
# print(list2)

# list2.remove(15)
# print(list2)

# list3 = [10,20]
# list4 = [30,40,50]
# list3.extend(list4)
# print(list3)


# tuple
# collection of "hetrogeneous" elememts
# () / tuple() constructor
# supports both positive & negative indexes
# position - 0
# immutable
# ocupies less memory compared to lists
# more performance compared to lists
# t1 = ("Python","FastAPI","LLMS","VectorDBS","RAGS","AgenticAI","Cloud")
# print(t1[0])
# print(t1[-1])
# t1[0] = "Python Framework"
# print(t1[::-1])

# import sys
# list1 = [10,20,30,40,50]
# t1 = (10,20,30,40,50)
# print(sys.getsizeof(list1))
# print(sys.getsizeof(t1))

# dictionary
# key - value pairs
# keys are "immutable" and values are "mutable"
# {} / dict() constructor
# d1 = {"num1":200,"num2":100}
# print(d1.keys())    # display only keys
# print(d1.values())  # display only values
# print(d1.items())   # display both key & value

# d1 = {"name":"VPro"}
# print(d1["name"])
# print(d1.get("name1","VPro Skills"))

# Set
# never allows duplicates
# {} / set()
s1 = {10,20,10,30,20,10}
print(s1)

s2 = {"Samba","Samba","samba"}
print(s2)

s3 = {1,1.0,True}   # 1 & 1.0 & 1 (meaning)
print(s3)


# None
emp = None
print(emp)

print(type(100))
print(type(100.12345))      # <class 'float'>
print(type("Hello"))
print(type(True))
print(type([]))

t1 = (10,20)
print(type(t1))

t2 = (100,)
print(type(t2))

d1 = {"key":"hello"}
print(type(d1))

# set = {10,20,30}
# print(type(set))

print(type(None))

x = set()       # empty set
print(type(x))


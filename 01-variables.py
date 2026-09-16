# Nested Tuple


# list1 = [[10,20,30],
#          [40,50,60],
#          [70,80,90]]
# for inner_list in list1:
#     for element in inner_list:
#         print(element)
#     print("------------------")



# list1 = ["QC","FDE","MLOps","LLOps","AgenticOps"]
# list2 = [10,20,30,40,50]
# for element1,element2 in zip(list1,list2):
#     print(element1,element2,sep="---->")


# list1 = [1000,2000,3000,4000,5000]
# for index,element in enumerate(list1):
#     print(index,element,sep="---->")

# list1 = [10,20,30,40,50]
# for element in list1:
#     print(element,end=" | ")


# t1 = tuple( range(10,1,-2) )      #10 8 6 4 2 
# print(t1)

# res2 = list( range(1,10,2) )       # 1 included, 10 excluded and step 2    # 1,3,5,7,9
# print(res2)

# t1 = tuple( range(1,5) )      #1 included and 5 excluded  1,2,3,4
# print(t1)

# res1 = list( range(5) )        
# print(res1)     # [0, 1, 2, 3, 4]

# num1 = 0.1
# num2 = 0.2
# num3 = num1 + num2
# print(num3) # 0.30000000000000004



# num1 = 0x123ABC
# print(num1)

# num2 = 0o123
# print(num2)

# num3 = 0b1010
# print(num3)



# from colorama import Fore
# num1 = 2_00     # 200
# num2 = 1_0_0    # 100
# add = num1 + num2
# print(Fore.RED + f"Addition : {add}")


# num1 = 10
# num2 = 3

# res = num1 / num2
# print(res)

# res1 = num1 // num2
# print(res1)

# res2 = num1 % num2
# print(res2)

# res3 = num1 ** num2
# print(res3)

# para = """
#     Course Includes
#         1) Python
#         2) ML + QC
#         3) DL
#         4) NLP
#         5) GenAI
#         6) AgenticAI
#         7) Deployment (AWS,Azure,GCP)
# """
# print(para)


# name = "emp1"
# age = 30
# msg = "{} age is {}".format(name,age)
# print(msg)



# name = "emp1"
# dept = "R&D"
# msg = f"{name} working in {dept}"
# print(msg)



# name = "VPro"
# wish = f"Welcome to {name}"
# print(wish)







# variables - are used to store the data
# Ex. msg = "Hello,VPro"
# "Hello" -- string, 100 -- int, 100.12345 -- float, True/False -- boolean, ........

# boolean
# True / False (T and F should be capital)
# True - 1
# False - 0
# Note : "boolean" is the child datatype of "int"

# flag = True
# print(flag)     # True

# flag1 = False
# print(flag1)

# print(True + True)
# print(1 + True + False + True + 0)
# print(True / False)
# print(False / True)

# print( issubclass(bool,int) )

# print( type(flag) )     # bool
# print( type(flag1) )    # bool


# list
# collection of "hetrogeneous" elements
# [] / list() constructor
# index starts from "0"
# mutable (able to "modify" the data)

# list1 = [10,20,30,40,50]
# 10 - pos (0) / neg (-5)
# 50 - pos (4) / neg (-1)
# print(list1[0], list1[-5])
# print(list1[4], list1[-1])
# print(list1[2], list1[-3])
# print(list1[0:2])       # index "0" included and index "2" excluded
# print(list1[:3])        # 0:3   # 0 - included and 3 - excluded
# print(list1[:0+4])      # 0:4   # 0 - included and 4 excluded
# print(list1[3:])        # index "3" to last index
# print(list1[-2:])       # -2 to last
# print(list1[-4:])       # -4 to last
# print(list1[-4:-2])     # -4 included and -2 excluded
# print(list1[::2])       # skips alternative element
# print(list1[::3])       # skips two alternative elements
# print(list1[::-1])      # reverse the list
# print(list1[::-2])        # while reversing, skip alternative element
# print(list1[::-3])       # while reversing skip two alternative elements
# list1[0] = 1000
# print(list1)

# tuple
# collection of "hetrogeneous" elements
# () / tuple() constructor
# index starts from "0"
# immutable (unable to "modify" the data)

# import sys
# tuple1 = (100,200,300,400,500)
# list1 = [100,200,300,400,500]
# print(sys.getsizeof(tuple1))        # 80
# print(sys.getsizeof(list1))         # 104

# tuple1 = (10,20,30,40,50)
# tuple1[0] = 1000

# tuple1 = (10,20,30,40,50)
# print(tuple1[0])








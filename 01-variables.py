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
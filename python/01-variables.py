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

# Tuple
# collection of hetrogeneous elements
# () / tuple()
# index starts from "0"
# Immutable
# allows duplicates

# t1 = (10,20,30,40,50)
# print(t1[0])
# print(t1[-3])
# print(t1[-1])
# print(t1[::2])
# print(t1[::3])
# print(t1[::-1])
# print(t1[::-2])


# t1 = (1000,2000,3000,4000,5000)
# e1,e2,e3,e4,e5 = t1
# print(e1,e2,e3,e4,e5,sep=" ➡️ ")


# t1 = (1000,2000,3000,4000,5000)
# e1,*list1 = t1
# a,b,c,d = list1
# print(a,b,c,d)

# t1 = ("Python","ML","DL","NLP","GENAI","AGENTICAI")
# x,*y,z = t1
# print(y)

# t1 = (10,20,30,10)
# t1[0] = 100
# print(t1.count(10))
# print(t1.count(20))
# print(t1.count(40))
# print(t1.index(10))


# key & value pairs - dictionary
# {} / dict()
# keys must be "immutable" and values are "mutable"

# d1 = {
#     "num1" : 200,
#     "num2" : 100
# }
# print(d1.keys())
# print(d1.values())
# print(d1.items())

# d1 = {
#     "num1" : 200,
#     "num2" : 100
# }
# print(d1["num1"])
# d1["num3"] = 300
# print(d1)

# d1 = {
#     (10,20,30) : (100,200,300)
# }
# print(d1[(10,20,30)])

# Set
# Never allowd duplicates
# {} / set()
# Unordered

# s1 = {10,20,30,10,20}
# print(s1)

# s1 = {"Python","Python","python"}
# print(s1)

# s1 = {1,True,1.0}
# print(s1)

# s1 = {1,True,1.0,False,0,0.0}
# print(s1)

# None (Empty / Blank)
# chair = None
# print(chair)


# string - "" / '' / """ """
# int - positive / negative / zero
# float - decimal
# boolean - True(1) / False(0)  -- child datatype of int
# List - mutable
# Tuple - immutable
# dictionary - key & value pairs
# Set - never allows duplicates
# None

# x = list( range(5) )            # 0,1,2,3,4
# print(x)

# y = tuple( range(1,10) )
# print(y)

# x1 = list( range(1,10,2) )
# print(x1)

# y1 = tuple( range(10,1,-2) )
# print(y1)

list1 = [10,20,30,40,50]
# for element in list1:
#     print(element,end=" | ")

for index,element in enumerate(list1):
    print(index,element,sep="---->")
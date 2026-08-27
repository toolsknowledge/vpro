# msg = "Python"
# print(msg)

# msg = "Hello"   #olH
# print(msg[0])
# print(msg[-5])

# print(msg[4])
# print(msg[-4])

# print(msg[0:2])
# print(msg[1:3]) # 1 and 2 included. and 3 excluded
# print(msg[2:])
# print(msg[:3])  # 0 - included and 3 - excluded

# print(msg[-3:])
# print(msg[-5:-3])   # "-5, -4" included and "-3 excluded"

# print(msg[::-1])
# print(msg[::-2])
# print(msg[::-3]) # oe

# print("Hello" * 3)
# msg = """
#     we will cover
#     1) Python Basics including libraries
#     2) ML + QC
#     3) DL
#     4) NLP
#     5) GenAI
#     6) AgenticAI
#     7) Cloud Deployment (AWS,AZURE,GCP)
# """
# print(msg)

# name = "VPro Skills"
# print(f"Welcome to {name}")

# emp_name = "Emp1"
# age = 40
# print(f"Employee name is {name} and his age is {age}")

# name = "VPro"
# name = "VPro Skills"
# print(name)


# name = "Employee1"
# dept = "R & D"
# print("Employee name is {} and related to {}".format(name,dept))


# cmp = "VPro Skills"
# dept = "Quantum Computing"
# print("{0} department availble in {1}".format(dept,cmp))


# print("Hello \n World")
# print("Age is \t 40")
# print("C:\\ProgramFiles\\demo.py")
# print('It\'s Python')
# print("I Said \"Good Morning !!!\" ")


# strings are (immutable)

# name = "vPro"       # VPro
# name[0] = "V"
# print(name)

# name = "vPro"
# print("V" + name[1:])



# int
# positive, negative,zeros
# num1 = 200
# num2 = 100
# add = num1 + num2
# print(f"Addition is {add}")


# num1 = 10
# res = num1 ** 2
# print(res)


# num1 = 123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789
# print(num1)

# num1 = 1_0_0
# num2 = 1_0_0_0
# print(num1 + num2)

# num1 = 0x123ABC
# print(num1)

# num2 = 0o123
# print(num2)

# num3 = 0b101010
# print(num3)


# bool
# True - 1 / False - 0
# bool is "child" datatype of "int"

# flag = True
# flag1 = False
# print(flag)
# print(flag1)

# print(True + True)
# print(1 + True + 1)
# print(True + False)
# print(True / False) # ZeroDivisionError: division by zero
# print(False / True)

# Empty - False, Zero - False, None - False
# print(bool(""))
# print(bool( [] ))
# print(bool( () ))
# print(bool( {} ))
# print(bool( set() ))
# print(bool( None ))
# print( bool( 0 ))
# print( bool(0.0) )
# print( bool(False) )

# print( bool("VPro") )
# print( bool([10]) )
# print( bool((100)))
# print( bool({"name":"Emp1"} ))
# print( bool({10,10,20}) )
# print(bool(100))
# print(bool(100.123))
# print(bool(-100))


# List
# collection of "hetrogeneous" and "indexed" elements
# [] / list() (list constructor)
# mutable (we can modify)
# list1 = [10,20,30,40,50]
# print(list1[0],list1[-5])
# print(list1[2],list1[-3])
# print(list1[0:2])
# print(list1[:3])
# print(list1[3:])
# print(list1[-2:])
# print(list1[-4:])
# print(list1[-5:-2]) # -5, -4, -3 included and -2 excluded
# print(list1[::-1])
# print(list1[::-2])
# print(list1[::-3])
# print(list1[::2])
# print(list1[::3])

# list1[0] = 1000
# print(list1)

# print(list1[-5::2])
# print(list1[-5::-2])


# Tuple
# collection of indexed and hetrogeneous elements
# () / tuple()
# immutable
# t1 = (10,20,30,40,50)
# print(t1[2])
# print(t1[-3])
# print(t1[:2])
# print(t1[2:])
# print(t1[:0+1]) # 0:1
# print(t1[::-1])
# print(t1[::-2])
# print(t1[::2])
# print(t1[::3])

# t1[0] = 1000

# import sys
# list1 = [10,20,30,40,50]
# tuple1 = (10,20,30,40,50)
# print(sys.getsizeof(list1))
# print(sys.getsizeof(tuple1))

# dictionary
# represent data in "key and value" pairs
# keys are "immutable" and values are "mutable"
# {} / dict()
# key and value separated with the help of ":"

# d1 = {
#     "name" : "VPro",
#     "batch" : 5,
#     "time" : "06.00AM(IST)"
# }
# print(d1["name"])
# print(d1["time"])
# print(d1.keys())
# print(d1.values())
# print(d1.items())


# Set
# never allows "duplicates"
# hetrogeneous
# {} / Set()
# unordered

# s1 = {10,20,30,10,20,40}
# print(s1)

# list1 = [10,20,10,30,20,40]
# print( set(list1) )

# tuple1 = ("Hello","Hello")
# print(set( tuple1) )


# None - Empty / Blank / No-Value

# chair = None
# print(chair)

# chair = None
# if chair == None:
#     chair = "Emp1"
# print(chair)


# num1,num2 = 200,100
# print(num1, num2, sep="✍︎")

# num1 = num2 = 1000
# res = num1 + num2
# print(res)

# num1,num2 = 100,200         # num1 = 100, num2 = 200 
# print(num1,num2)

# num2,num1 = num1,num2
# print(num1,num2)

# str = "VPro"
# print(type(str))

# list1 = [10,20,30,40,50]
# print(type(list1[0]))

# chair = None
# print(type(chair))

# num1 = 0.2
# print(type(num1))

# x = {}
# x["name"] = "Franco"
# print(x)

# y = set()
# print(type(y))

# == (compares values)
print(100 == 100)

list1 = [10,20,30]
list2 = [10,20,30]
print(list1 == list2)

t1 = (10,20,30)
t2 = (10,20,30)
print(t1 == t2)

print(list1 is list2)

# s1 = {10,20,30}
# s2 = {10,20,30}
# s2 = s1
# print(s1 == s2)
# print(s1 is s2)









   
































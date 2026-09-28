"""
    varaibles
    *********
        variables are used to store the data
        Ex.
            string
            number
            boolean
            list
            tuple
            ---
            ---
            ---
        by default python is dynamically typed

        python supports below datatypes
        1) string
        2) int
        3) boolean
        4) list
        5) tuple
        6) dictionary
        7) set
        8) None
"""

"""
    int
    ***
        integer datatype supports positive/negative/zero
"""
# from colorama import Fore
# num1 = 200
# num2 = 100
# add = num1 + num2
# print(add)
# print(f"Addition : {add}")
# print("Addition : {}".format(add))
# print(Fore.GREEN + "Addition :",add)

# Subtraction
# Multiplication
# Division

# num1 = 0x123ABC
# print(num1)

# num2 = 0o123
# print(num2)

# num3 = 0b1010
# print(num3)


# num1 = 2_00     # 200
# num2 = 1_0_0    # 100
# print(num1 + num2)


# num1 = 100
# print(type(num1))


# x = 0.1
# y = 0.2
# z = x + y
# print(z)
# print(type(z)) 



"""
    Boolean
        1) True & False
        2) "T" must be capital and "F" must be the Capital
        3) Boolean is the child datatype of "int"
        4) True - 1 & False - 0
"""
# flag = True
# flag1 = False
# print(flag)
# print(flag1)

# print(True + True)
# print(1 + True + 1 + False)
# print(True/False)
# print(False/True)

# flag = True
# print(type(flag))
# print(issubclass(bool, int))


# # string
# # " ", ' ', """ """(paragraphs)
# str = "Hello"
# print(str[0])       # H
# print(str[-1])      # 0
# print(str[1])       # e
# print(str[::2])     # Hlo
# print(str[::3])     # Hl
# print(str[::-1])    # olleH
# print(str[::-2])    # olH
# print(str[::-3])    # oe


# str = "Welcome"
# print(str[0:2])     # 0 included and 2 excluded
# print(str[:3])  # 0:3 Wel
# print(str[3:])


# str = "hello"       # h - H (immutable)
# # str[0] = "H"

# str = "H" + str[1:]
# print(str)      # Hello

# str = 'Hello,Vpro !!!'
# print(str)

# msg = """
#     1) FDE (Forward Deployed Engineer)
#     2) Quantum Computing
#     3) Agentic AI
# """
# print(msg)

# list - collection of "hetrogeneous" elements called as "list"
# [] / list()
# mutable
# index starts from "0" / supprts negative indexes
# list1 = [10,20,30,40,50]
# 10 - 0 & -5
# 30 - 2 & -3
# print(list1[0])
# print(list1[-1])
# print(list1[-3])
# print(list1[::2])
# print(list1[::3])
# print(list1[::-1])
# print(list1[::-2])
# print(list1[::-3])
# print(list1[0:2])       # 0&1 included and 2 excluded
# print(list1[:3])        # 0:3 - 0,1&2 included and 3 excluded
# print(list1[3:])        # index 3 to end
# print(list1[-3:])       # -3 to end
# print(list1[-5:-3])     # -5 & -4 included and -3 exclude

# list1 = [10,20,30,40,50]
# list1[0] = 1000
# print(list1)        # [1000, 20, 30, 40, 50] (mutable)


# tuple
# collection of "hetrogeneous elements" called as "tuple"
# () / tuple() constructor
# immutable (we can't modify)
# index starts from "0" and supports "negative" indexes
# t1 = ("Python","ML","DL","NLP","GenAI","AgenticAI")
# print(t1[-6])   # Python
# print(t1[5])    # AgenticAI
# print(t1[::-1]) # reverse
# print(t1[4:])   # index 4 to last
# print(t1[-2:])  # index -2 to last
# print(t1[::3])  # skip every two alternative elements


# t1 = (10,20,30,40,50)
# t1[4] = 500


# Set
# never allows "duplicates"
# {} / set() constructor
# unordered
# hetrogeneous elements
# s1 = {10,20,30,10,20}
# print(s1)


# dictionary
# key & value pairs
# {} / dict() constructor
# keys are "immutable" and values are "mutable"
# d1 = {
#     "num1" : 200,
#     "num2" : 100
# }
# print(d1.keys())    # read only keys
# print(d1.values())  # read only values
# print(d1.items())   # read both key and value

# None
# blank / empty
# chair = None
# print(chair)
# if chair == None:
#     chair = "Emp1"
# print(chair)
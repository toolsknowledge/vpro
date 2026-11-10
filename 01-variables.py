"""
    variable
    ********
        variables are used to store the data
        Ex.
            String
                Ex.     "VPro"
            Integer
                Ex.      100
            Boolean
                Ex.     True / False
            ---
            ---
            ---
        python supports the below datatypes
        1) String
        2) Integer
        3) Float
        4) Boolean
        5) List
        6) Tuple
        7) Dictionary
        8) None

    String
    ******
        collection of characters called as String
        we will create String in 3 ways
        1) "" (double quotes)
        2) '' (single quotes)
        3) """ """ (triple quotes)

    Integer
    *******
        whole number called as Integer
        Positive Number
        Negative Number
        Zero

    Float
    *****
        Fractional values called as Float
        Ex.
            100.12345

    Boolean
    *******
        supports two Boolean Values
        1) True (T Should be Capital)
        2) False (F Should be Capital)

        True - 1
        False - 0

    Boolean is the Child DataType of Integer

    List
    ****
        "collection" of elements
        "hetrogeneous" elements
        list supports both "positive/negative" indexes
        positive index starts from "0"
        negative index starts from "-1"
        [] / list() constructor
        by default list is "mutable"

    tuple
    *****
        () / tuple()
        immutable

"""

# str = "VPro !!!"
# print(str)

# sub = 'Python'
# msg = f"Welcome to {sub}"
# print(msg)


# x = "Python"
# y = "FastAPI"
# z = "VectorDB"
# msg = "we will cover {} as a framework, backend as {} and database as {}".format(x,y,z)
# print(msg)

# msg = """
#     we will cover:
#     Module 1: Python
#     Module 2: FastAPI
#     Module 3: LLMS
#     Module 4 : VectorDBS
#     Module 5: RAGS
# """
# print(msg)

# num1 = 200
# num2 = 100
# add = num1 + num2
# print(add)
# print(f"Addition : {add}")
# print("Addition : {}".format(add))

# sub = num1 - num2


# temp = 96.3
# print(temp)


# flag = True
# flag1 = False
# print(flag)
# print(flag1)

# print(True + 1)
# print(True + False)
# print(True / False)
# print(False / True)

# x = "Hello"
# print(type(x))
# y = 100
# print(type(y))
# z = 100.12345
# print(type(z))
# f = True
# print(type(f))
# print(isinstance(f,int))


# list1 = [10,20,30,40,50]
# 10 --- 0, -5
# 20 --- 1. -4
# 50 --- 4  -1
# print(list1[0])
# print(list1[-4])
# print(list1[4])
# print(list1[-2])

# print(list1[::2])     # [10, 30, 50]
# print(list1[::3])     # [10, 40]

# print(list1[::-1])    # [50, 40, 30, 20, 10]
# print(list1[::-2])    # [50, 30, 10]
# print(list1[::-3])    # [50, 20]


# list2 = [100,500,200,400,300]
# print(max(list2))
# print(min(list2))
# print(sum(list2))
# print(len(list2))
# print(sum(list2) / len(list2))


# list3 = [1,5,2,4,3]
# res = sorted(list3)     # sorted() -- immutable function
# print(res)      # [1, 2, 3, 4, 5]
# print(list3)    # [1, 5, 2, 4, 3]


# list4 = [1000,5000,2000,4000,3000]
# list4.sort(reverse=True)        # sort() -- mutable function
# print(list4)        # [1000, 2000, 3000, 4000, 5000]    #[5000, 4000, 3000, 2000, 1000]


# list5 = [1,2,3,4,5]
# list5[0] = 1000
# print(list5)


# list6 = ["Python","ML","DL","NLP","GenAI","AgenticAI"]
# list6.sort()
# print(list6)


# list7 = ["Apple",10,10.0,True]
# list7.sort()
# print(list7)


# l1 = [10,100,1000,10000,100000]
# 10 - 0 & -5
# 100000 - 4 & -1
# print( l1[0] )
# print( l1[-1] )

# access 100 with positive index
# access 1000 with negative index


# l2 = [1,2,3,4,5]
# l2[0] = 100
# l2[4] = 500
# print(l2)

# l3 = [10,20,30,40,50]
# print(l3[0:2])      # 0 - included and 2 excluded
# print(l3[:3])       # 0:3   0 - included and 3 excluded
# print(l3[1:3])   
# print(l3[2:])       # index 2 to end   
# print(l3[:1+1+1])   # 0:3
# print(l3[-2:])
# print(l3[-4:])
# print(l3[-5:-2])


# l4 = [10,30,40]
# l4.append(50)
# print(l4)           # [10, 30, 40, 50]

# l4.insert(1,20)
# print(l4)           # [10, 20, 30, 40, 50]

# l5 = [60,70]
# l4.extend(l5)
# print(l4)           # [10, 20, 30, 40, 50, 60, 70]


# l6 = [10,20,30,40,50]
# l6.remove(20)
# print(l6)               # [10, 30, 40, 50]

# l6.pop(2)
# print(l6)               # [10, 30, 50]


# l7 = [10,20,30,40,50]
# del l7[0]
# print(l7)       # [20, 30, 40, 50]

# del l7[1:3]
# print(l7)

# l7.clear()
# print(l7)

# l8 = [10,20,10,20,40,10]
# l8.remove(10)
# print(l8)       # [20, 10, 20, 40, 10]


# l9 = [10,50,20,40,30]
# print(len(l9))
# print(max(l9))
# print(min(l9))
# print(sum(l9))
# print(sum(l9) / len(l9))

# res = sorted(l9)
# print(res)


# l10 = [10,50,20,40,30]
# print( l10[::-1] )


# l11 = [10,20,30,40,50]
# print( l11[::2] )     # [10, 30, 50]
# print( l11[::3] )
# print( l11[::-1] )
# print( l11[::-2] )
# print( l11[::-3] )


# t1 = (10,20,30,40,50)
# t1[0] = 1000

# import sys
# l1 = [10,20,30,40,50]
# t1 = (10,20,30,40,50)
# print(sys.getsizeof(l1))
# print(sys.getsizeof(t1))


t1 = (10,20,30,40,50)
print(t1[0])
print(t1[-1])
print(t1[0:2])
print(t1[-2:])


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
        collection of elements called as list
        list allows hetrogenous
        [] / list()
        index starts from 0
        supports negative indexes also Ex. -1
        mutable(modify)
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
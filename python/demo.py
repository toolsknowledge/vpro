# 4 videos - 1


# chair = None
# print(chair)


# set
# set, never allows "duplicates"
# s1 = {10,20,30,10,20,40}
# print(s1)


# dictionary
# d1 = {
#     "key1" : "Hello",
#     "key2" : "Welcome"
# }
# print(d1["key1"])
# print(d1["key2"])
# print(d1.keys())
# print(d1.values())
# print(d1.items())




# tuple1 = (10,20,30,40,50)     # () / tuple()
# print(tuple1[0:3])      #0,1,2 -- included. and 3 onwards excluded
# print(tuple1[2:4])
# tuple1[0] = 1000


# print(tuple1[0])
# print(tuple1[-4])
# print(tuple1[2])
# print(tuple1[-2])
# print(tuple1[4])









# list1 = [10,20,30,40,50]
# print(list1[0])
# print(list1[-5])
# print(list1[4])
# print(list1[2])
# print(list1[0:2])
# print(list1[:3])        #0:3
# print(list1[1:4])       # index "1" included and index "4" excluded
# print(list1[::2])
# print(list1[::3])
# print(list1[::-1])      # reversing
# print(list1[::-2])      # skip single element [50,30,10]


# list1 = [10,20,30,40,50]
# list1[0] = 1000
# print(list1)










"""
    "VPro" --  String 
    100 - int
    100.12345 - float
    True / False - Boolean
    [10,20,30,.....] - List (Mutable)
    (100,200,300,.....) - Tuple (Immutable)
    {"name":"vpro"} - dictionary
    {10,20,10,30} - {10,20,30} - Set
    None - Empty / Blank
"""

"""
    List
"""

# subs = ["Python","ML","DL","NLP","GenAI","AgenticAI"]
# s1,*subs1,s6 = subs
# a,b,c,d = subs1
# print(a,b,c,d)



# list2 = [100,200,300,400,500]
# e1, *my_list = list2
# print(my_list)



# list1 = [10,20,30,40,50]
# a,b,c,d,e = list1
# print(a,b,c,d,e,sep="--->")


# print(list1[0])
# print(list1[-1])
# print(list1[::2])
# print(list1[::3])
# print(list1[::-1])
# print(list1[::-3])
# print(list1[0:3])
# print(list1[:2])    # 0:2
# print(list1[2:])
# print(list1[3:])
# print(list1[-3:])
# print(list1[-2:])
# print(list1[-5:-2])
# list1[2] = 3000
# print(list1)

"""
    tuple
    *****
        collection of hetrogeneous elements called as tuple
        ()
        0
        immutable
"""

# import sys
# list1 = [10,20,30,40,50]
# tuple1 = (10,20,30,40,50)
# print(sys.getsizeof(list1))
# print(sys.getsizeof(tuple1))

# tuple1 = (10,20,30,40,50)
# tuple1[0] = 100


# tuple1 = (1000,2000,3000,4000,5000)
# print(tuple1[0])
# print(tuple1[-1])
# print(tuple1[0:2])


# dictionary
# d1 = {
#     "course" : "agentic-ai",
#     "deploy" : "aws"
# }
# print(d1.keys())
# print(d1.values())
# print(d1.items())

# Set
# s1 = {10,20,30,10,20,40}
# print(s1)

# None (Empty / Blank)
# chair = None
# print(chair)
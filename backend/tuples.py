# Tuples
# collection of hetrogeneous elements 
# index based (Positive Index - 0 (left to right)) (Negative Index - 1 (right to left))
# () / tuple()

# Example-1
# t1 = (10,20,30,40,50)
# print(type(t1))                 # <class 'tuple'>

# t2 = 10,20,30
# print(type(t2))                 # <class 'tuple'>

# t3 = (10)
# print(type(t3))                 # <class 'int'>

# t4 = (10,)
# print(type(t4))                 # <class 'tuple'>

# t5 = 10,
# print(type(t5))                 # <class 'tuple'>


# Example-2
# t1 = 10,20,30,40,50
# unpack to e1,e2,e3,e4,e5


# Example-3
# t1 = 100,200,300,400,500
# e1, *list1 = t1
# print(list1)            # [200, 300, 400, 500]


# Example-4
# t1 = 10,100,1000,10000,100000
# e1 - 10
# e4 - 10000
# e5 - 100000
# list - [100,1000]


# Example-5
# t1 = (10,20,30)
# list1 = list(t1)
# print(list1)

# t2 = tuple(list1)
# print(t2)


# Example-6
# t1 = 100,200,300,400,500
# print(t1[0:2])      # 0 onwardsincluded & 2 onwards excluded
# # display 100,200, 300

# # display 300,400


# print(t1[2:])           # index 2 to end
# # display 200,300,400,500

# # display 400, 500

# print(t1[-2:])      # index -2 to end

# # display from 30, 40, 50 with negative indexes

# # display 20, 30, 40 and 50 with negative indexes

# print(t1[-5:-2])        # -5 onwards included and -2 onwards excluded



# Example - 7
# t1 = 10,50,20,40,30
# max, min, count, sum, avg
# sort ( sorted() )


# Example-8 (Swap)
# a = 10
# b = 20
# b,a = a,b  # packing
# print(a,b)      # 20 10


# Example-9
# t1 = 10,10,10,20,20,20
# print(t1.count(20))
# print(t1.index(20))
# print(t1.index(10))
# find index of 2nd 20
# find index of third 10


# Example-10
# t1 = 10,20
# t2 = 30,40
# t3 = t1 + t2
# print(t3)

# t4 = t3 * 2
# print(t4)

# print(10 in t4)
# print(100 in t4)


# Example - 11
# import sys
# t1 = 10,20
# list1 = [10,20]
# print(sys.getsizeof(t1))
# print(sys.getsizeof(list1))


# Example-12
# t1 = 10,20
# t1[0] = 100     # Err

# list1 = list(t1)
# list1[0] = 100

# t1 = tuple(list1)
# print(t1)


# Example-13
# d1 = {
#     [10,20] : "Hello"           # Err
# }

# d2 = {
#     (10,20) : "Hello"           # Allowed
# }


# Example-14
# t1 = (10,20)
# t2 = t1 + (30,)
# print(t2)


# Example-15
# t1 = (10,20,30)
# print(id(t1))           # 4376097600

# t1 = t1 + (40,)
# print(id(t1))           # 4306992992



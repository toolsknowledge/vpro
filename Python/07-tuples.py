# tuple
# collection of "ordered elements"
# immutable
# ()
# index starts from "0" and supports "negative indexes" also

# Example-1
# t1 = (10,20,30)
# print(type(t1))

# t2 = (100)
# print(type(t2))

# t3 = (1000,)
# print(type(t3))

# t4 = 10000,
# print(type(t4))

# t5 = 10000,2000,3000
# print(type(t5))

# t6 = tuple([10,20,30])
# print(type(t6))


# Example-2
# t1 = (10,20,30)

# list1 = list(t1)    # tuple -- list
# list1[0] = 100

# t2 = tuple(list1)  # list -- tuple
# print(t2)
# print(t1)       # never modified


# Example - 3
# t1 = 10,20,30,40,50
# print(t1[0],t1[-5])
# print(t1[2],t1[-3])
# print(t1[0:3])
# print(t1[:2])
# print(t1[2:])
# print(t1[-3:])
# print(t1[-4:-1])


# Example-4
# t1 = (10,20,30,40,50,10,20)
# print(t1.count(10))
# print(t1.count(50))
# print(t1.index(20))
# print(t1.index(30))

# t1 = 10,20,30,40,50
# e1,e2,e3,e4,e5 = t1
# print(e1,e2,e3,e4,e5)

# t2 = 10,20,30,40,50
# e1,*e2,e3 = t2      # e2 = [20,30,40]
# a1,*a2 = e2         # a2 = [30,40]
# x,y = a2
# print(e1,a1,x,y,e3)


# def test():
#     return 10,20,30

# t1 = test()
# e1,e2,e3 = t1
# print(e1,e2,e3)

# a,b = 10,20
# b,a = a,b
# print(a,b)

# t1 = ((10,20),(30,40),(50,60))
# for inner_t1 in t1:
#     for index,element in enumerate(inner_t1):
#         print(index,element,sep="---->")


# t1 = ([10,20],[30,40])
# t1[0] = 100
# t1[0][0] = 100
# print(t1)


# t1 = (10,20)
# t2 = (30,40)
# t3 = t1 + t2
# t4 = t3 * 2
# print(30 in t4)
# print(300 in t4)
# print(300 not in t4)

# d1 = {
#     [10,20] : "Hello"
# }

# d1 = {
#     (10,20) : "Hello"
# }

# print(hash((1,2,3)))
# print(hash([1,2,3]))

import sys
print(sys.getsizeof([10,20,30]))
print(sys.getsizeof((10,20,30)))

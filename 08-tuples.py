# tuples
# 1) Ordered 2) Immutable 3) Allows Duplicates 4) Faster Compared to Lists 5) Ocupies less space 6) () 7) Hetrogeneous

# Faq5 (Avg Marks)
# marks = (50,55,60,75,70)
# print(sum(marks) / len(marks))

# Faq4
# stds = ("Std1","Std2")
# marks = (90,100)
# res = tuple(zip(stds,marks))
# print(res)


# Faq3
# res = [x*x for x in range(5)]
# print(res)

# Faq2
# tuple1 = 10,20,30
# tuple2 = 10,20,30
# print(tuple1 == tuple2)
# print(tuple1 is tuple2)

# Faq1
# t1 = (10,20,30)
# print(id(t1))

# t1 = t1 + (40,)
# print(id(t1))


# Example - 11
# d1 = {
#     (10,) : 10
# }
# print(d1)


# Example-10
# tuple1 = (10,20)
# tuple2 = (30,40)
# tuple3 = tuple1 + tuple2
# print(tuple3)
# tuple4 = tuple3 * 3
# print(tuple4)
# print(10 in tuple4)
# print(100 in tuple4)
# print(10 not in tuple4)
# print(100 not in tuple4)



# Example - 9 
# tuple1 = (10,20,30,40,50)
# for element in tuple1:
#     print(element)

# for index,value in enumerate(tuple1):
#     print(index,"-->",value)

# tuple2 = ((10,20),(30,40),(50,60))
# for inner_tuple in tuple2:
#     for index,value in enumerate(inner_tuple):
#         print(index,"--->",value)
#         print("-----------")



# Example - 8
# tuple1 = 10,20,30,40,50,10,20
# print(f"Number of Elements : {len(tuple1)}")
# print(f"Max  Elements : {max(tuple1)}")
# print(f"Min of Elements : {min(tuple1)}")
# print(f"Sum of Elements : {sum(tuple1)}")
# print(f"10 Repeated : {tuple1.count(10)}")
# print(f"Index of First Occured Element : {tuple1.index(10)}")
# tuple2 = (10,50,20,40,30)
# print(tuple(sorted(tuple2)))


# Example - 7
# def test():
#     return 10,20,30

# e1,*e2 = test() # e2 = [20,30]
# *x,y = e2 # x = [20]
# a, = x
# print(a,e1,y)

# Example - 6
# tuple1 = (10,20,30,40,50)
# e1,e2,e3,e4,e5 = tuple1
# print(e1,e2,e3,e4,e5)

# tuple2 = 100,200,300,400,500
# e1, *e2, e3 = tuple2
# x,*y = e2
# *a,b = y
# z, = a
# print(e1,x,z,b,e3)


# Example - 5
# tuple1 = (10,[20,30])
# tuple1[1][0] = 200
# print(tuple1)


# Example-4
# tuple1 = (10,20,30,40,50)
# tuple1[0] = 100 # TypeError: 'tuple' object does not support item assignment
# list1 = list(tuple1)
# list1[0] = 100
# tuple1 = tuple(list1)
# print(tuple1)

# Example-3
# tuple1 = (10,20,30,40,50)
# print(tuple1[0])
# print(tuple1[-5])
# print(tuple1[0:3])
# print(tuple1[:2])
# print(tuple1[-3:-1])
# print(tuple1[3:])
# print(tuple1[-3:])
# print(tuple1[::-1])


# Example-2
# import sys
# list1 = [10,20,30,40,50]
# tuple1 = (10,20,30,40,50)
# print(sys.getsizeof(list1))
# print(sys.getsizeof(tuple1))



# Example-1
# t1 = (10,20,30)
# t2 = 100,200,300
# t3 = "Hello",
# print(t1,end=" ")
# print(t2,end=" ")
# print(t3,end=" ")
# print(type(t1),type(t2),type(t3))
# t4 = (10)
# print(type(t4))
# t5=("Hello")
# print(type(t5))
# t6 = ("VPro",)
# print(type(t6))


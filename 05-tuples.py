# collection of indexed,hetrogeneous elements called as tuple
# immutable
# () / tuple()

# import sys
# list1 = [10,20,30,40,50]
# tuple1 = (10,20,30,40,50)
# print(sys.getsizeof(list1))
# print(sys.getsizeof(tuple1))


# tuple1 = 10,20,30,40,50
# e1,e2,e3,e4,e5 = tuple1
# print(e1,e2,e3,e4,e5)


# t1 = (10,)
# print(type(t1))


# t1 = 10,20,30,40,50
# e1,*list2,e5 = t1       # list2 = [20,30,40]
# *list3,e4 = list2       # list3 = [20, 30]
# e2,e3 = list3
# print(e1, e2, e3, e4, e5)


# t1 = 10,20,30,40,50
# list1 = list(t1)
# print(list1)

# list1 = ["Python","ML","DL","NLP","GenAI","AgenticAI"]
# tuple1 = tuple(list1)
# print(tuple1)

# t1 = 10,50,20,40,30
# print(len(t1))
# print(max(t1))
# print(min(t1))
# print(sum(t1))
# print(t1.count(10))
# print(t1.index(20))

# res = tuple( sorted(t1) )
# print(res ,"\n", t1)

# t1 = 10,50,20,40,30,None
# print(sorted(t1))

# t1 = ["Hello","Welcome","Hi",10]
# print(sorted(t1))


# t1 = 10,200,3000,30000,300000,20
# t2 = 100,1000,10000,100000,2,2
# for element in t1:
#     print(element)

# print( *("Vpro" for _ in t1) )

# for index,element in enumerate(t1):
#     print(index,element)

# for element1,element2 in zip(t1,t2):
#     print(element1,element2)

# t1 = ((10,20,30),
#       (40,50,60),
#       (70,80,90))
# for inner in t1:
#     for element in inner:
#         print(element, end=" ")
#     print("\n")


# def test():
#     num1,num2 = 200,100
#     return num1 + num2, num1 - num2, num1 * num2, num1 / num2, num1, num2

# t1 = test()
# add,sub,mul,div,n1,n2 = t1
# print(add,sub,mul,div,n1,n2)


# t1 = 10,20,30,40,50
# print(30 in t1)
# print(300 in t1)
# print(3000 not in t1)

# d1 = {
#     (10,20) : (10,20)
# }
# print(d1[(10,20)])


# t1 = 10,20
# t2 = 30,40
# t3 = t1 + t2
# t4 = t3 * 2
# print(t4)

# t1 = (10,20,30,40,50)
# t1[0] = 1000

t1 = 10,20,30,40
t2 = t1 + (50,)

res = t2[:2] + (25,) + t2[2:]
print(res)












"""
    tuple
    *****
        collection of hetrogeneous elements
        allows duplicates
        () / tuple()
        index starts from "0" / supports negative indexes
        immutable
"""
# Example-1 (unpacking)
# t1 = (10,20,30,40,50)
# e1,e2,e3,e4,e5 = t1
# print(e1,e2,e3,e4,e5)

# Example-2
# t1 = (100,200,300,400,500)
# e1,*list2,e5 = t1       # [200,300,400]
# e2,*list3 = list2       # [300,400]
# e3,e4 = list3
# print(e1,e2,e3,e4,e5)

# Example-3
# t1 = 10,20,30,40,50
# print(t1)
# print(type(t1))

# t2 = 10,
# print(t2)
# print(type(t2))

# t3 = 100
# print(t3)
# print(type(t3))

# Example-4
# def calc(num1,num2):
#     return num1+num2, num1-num2, num1*num2, num1/num2

# t1 = calc(200,100)
# add,sub,mul,div = t1
# print(add,sub,mul,div)

# Example-5
# t1 = 10,20,10,10.0,20,20,30,10,40
# print(t1.count(10))
# print(t1.count(20))
# print(t1.count(50))
# print(t1.index(20))
# print(t1.index(10.0))


# Example-6
# t1 = 10,20,30,40,50
# list1 = list(t1)            # tuple - list
# list1[0] = 100
# t1 = tuple(list1)           # list - tuple
# print(t1)



# Example-7
# import sys
# list1 = [10,20,30,40,50]
# tuple1 = (10,20,30,40,50)
# print(sys.getsizeof(list1))
# print(sys.getsizeof(tuple1))


# Example-8
# t1 = 10,50,20,40,30
# print(max(t1))
# print(min(t1))
# print(len(t1))
# print(sum(t1))
# res = tuple( sorted(t1) )
# print(res)


# Example-9
# t1 = 10,20,30,40,50
# print(30 in t1)
# print(300 not in t1)
# print(300 in t1)


# Example-10
# num1 = 200
# num2 = 100
# num2,num1 = num1,num2
# print(num1,num2)

# Example-11
# from colorama import Fore
# t1 = 10,20,30,40,50
# t2 = 100,200,300,400,500
# for element in t1:
#     print(Fore.RED + str(element),end=" ")

# for index,element in enumerate(t1):
#     print(index,element,sep="--->")

# for element1,element2 in zip(t1,t2):
#     print(element1,element2)


# Example-12
# t1 = ((10,20),(30,40),(50,60),(70,80),(90,100))
# for inner in t1:
#     for index,element in enumerate(inner):
#         print(index,element)


# Example-13
# t1 = (10,20,30,40,50)
# print(t1[::4])
# print(t1[::-5])
# print(t1[-3:-1])

# Example-14
# keys must be immutable (dict)
# we can use tuples as dict keys
# d1 = {
#     (10,20) : (10,20)
# }
# print(d1)


# Example-15
numbers = [10,50,20,30,20]
largest = numbers[0]
for num in numbers:
    if num > largest:
        largest = num

print(largest)










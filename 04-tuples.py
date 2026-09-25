"""
    tuple
    *****
        collection of "hetrogeneous" elements called as "tuple"
        index starts from "0"
        tuples will support "negative" indexes also
        we will represent tuples with the help of "() / tuple()"
        tuples are "immutable"
"""

# t1 = (100,200,300,400,500)
# t1[0] = 1000


# t1 = (100,200,300,400,500)
# e1,e2,e3,e4,e5 = t1
# print(e1,e2,e3,e4,e5)


# t1 = (1000,2000,3000,4000,5000)
# e1,*list1,e2 = t1
# x, *y = list1
# a,b = y
# print(e1,x,a,b,e2)


# t1 = (10,20,10,10,20,30,40,50,10)
# print(t1.count(10))
# print(t1.count(20))
# print(t1.count(100))


# t1 = (100,20,30,20)
# print(t1.index(20))
# print(t1.index(100))
# print(t1.index(30))


# t1 = (100,200,300,400,500)
# for element in t1:
#     print(element,end=" | ")



# t1 = (10,20)
# t2 = (30,40)
# t3 = (50,)
# t4 = t1 + t2 + t3
# t5 = t4 * 2
# print(t4)
# print(t5)


# t1 = 10,20,30,40,50
# for index,element in enumerate(t1):
#     print(index,element)


# t1 = 10,20,30,40,50
# t2 = 100,200,300,400,500
# for element1,element2 in zip(t1,t2):
#     print(element1,element2)

# import sys
# list1 = [10,20,30,40,50]
# t1 = (10,20,30,40,50)
# print(sys.getsizeof(list1))
# print(sys.getsizeof(t1))


# t1 = 10,20,30,40,50
# list1 = list(t1)        # list() tuple - list
# list1[0] = 100
# t1 = tuple(list1)       # tuple() list - tuple
# print(t1)


# def calc(num1,num2):
#     return num1+num2, num1-num2, num1*num2, num1/num2

# e1,e2,e3,e4 = calc(200,100)
# print(e1,e2,e3,e4)


# t1 = 100,500,200,400,300
# print(max(t1))
# print(min(t1))
# print(len(t1))
# print(sum(t1))
# print(sum(t1)/len(t1))
# res = sorted(t1)
# print(res)


# t1 = (10,20,30,40,50)
# print(30 in t1)
# print(300 not in t1)


# t1 = ((10,20,30),
#       (40,50,60),
#       (70,80,90))
# for inner in t1:
#     for index,element in enumerate(inner):
#         print(index,element,sep="→")
#         print("-------------")


# dictionary
# keys - immutable
# values - mutable

# d1 = {
#     (10,20) : "VPro"
# }
# print(d1)

# t1 = (10,20,30,40,50)
# found = False
# e1 = input("Enter Element : ")
# for element in t1:
#     if element == int(e1):
#         found = True

# res = "Element Found" if found else "Element Not Found"
# print(res)




# t1 = (10,50,20,40,30,100)
# large = t1[0]       # 100
# for element in t1:
#     if element>large:
#         large = element

# print(large)


# t1 = (10,20,30,40,50)
# print(type(t1))     # <class 'tuple'>

# l1 = list(t1)           # list() -- tuple to list
# print(type(l1))

# l1[0] = 100
# print(l1)

# t1 = tuple(l1)
# print(t1)


# t1 = ([10],[20],[30])
# t1[0][0] = 100
# print(t1)

# num1 = 200
# num2 = 100
# num2,num1 = num1,num2
# print(num1,num2)

t1 = (10,20,30,40,50)
print(*t1)



















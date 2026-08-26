# collection of indexed and hetrogeneous elements called as list
# [] / list() constructor
# immutable
# slicing

# list1 = [10,20,30,40,50]
# e1,e2,e3,e4,e5 = list1
# print(e1, e2, e3, e4, e5)


# list1 = [1000,100,10,0,-10]
# ele1, *list2, ele5 = list1
# ele2, *list3 = list2
# ele3, ele4 = list3
# print(ele1,ele2,ele3, ele4, ele5)

# list1 = [10,50,20,40,30]
# print(len(list1))
# print(max(list1))
# print(min(list1))
# print(sum(list1))

# list2 = [10,20,10,30,10,20,20,30,40,20]
# print(list2.count(10))
# print(list2.count(20))
# print(list2.count(100))

# list3 = [100,10,0]
# print(sum(list3) / len(list3))


# list4 = [10,50,20,40,30]
# res = sorted(list4)
# print(res)
# print(list4)

# list5 = [10,50,20,40,30]
# list5.sort()
# print(list5)


# list1 = [10,20,30]
# list1.append(40)
# list1.append(60)
# list1.insert(4,50)
# list2 = [70,80,90,100]
# list1.extend(list2)
# print(list1)

# list1 = [10]
# list2 = [20,30]
# list1.extend(list2)
# list1.append(list2)
# print(list1)

# list1 = [10,20,10,20,30,40,50,10]
# list1.remove(10)
# list1.pop()
# list1.clear()
# print(list1)


# list1 = [10,20,30,40,50]
# del list1[0]
# print(list1)

# list1.remove(10)
# print(list1)

# del list1[1:3]
# print(list1)


# list1 = [10,20,30,40,50]
# print(30 in list1)
# print(300 not in list1)
# print(60 in list1)


# list1 = [10,20,30,40,50]
# print(list1[::-1])
# list1.reverse()
# print(list1)

list1 = [10,20,30,40,50]
# for element in list1:
#     print(element,end=" ")

# for index,element in enumerate(list1):
#     print(index,element,sep="--->")

i=0
while i<len(list1):         # 1 < 5
    print(list1[i])         # list1[1]
    i = i+1                 # i = 2
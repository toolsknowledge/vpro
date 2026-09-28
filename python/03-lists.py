"""
    collection of "hetrogeneous" and "indexed" elements called as "list"
    we will represent list with the help of either [] / list()
    list is mutable
"""

# list1 = [10,50,20,40,30]
# print(max(list1))
# print(min(list1))
# print(len(list1))
# print(sum(list1))
# print(sum(list1) / len(list1))

# res = sorted(list1)
# print(res)          # [10, 20, 30, 40, 50]
# print(list1)        # [10, 50, 20, 40, 30]


# list1 = ["Python","ML","DL","NLP","GenAI","AgenticAI"]
# print(list1[0])
# print(list1[-1])
# print(list1[:2])        # 0 included and 2 excluded
# print(list1[-2:])
# print(list1[2:5])       # 2 included and 5 excluded
# print(list1[-4:-1])
# print(list1[::-1])


# list1 = [10,20,30,40]
# list1.append(60)
# print(list1)            #[10,20,30,40,60]

# list1.insert(4,50)
# print(list1)            #[10,20,30,40,50,60]

# list2 = [70,80]
# list1.extend(list2)
# print(list1)            #[10, 20, 30, 40, 50, 60, 70, 80]


# list1.append(10)
# list1.append(20)
# print(list1)            #[10, 20, 30, 40, 50, 60, 70, 80, 10, 20]


# print(list1.count(10))      #2
# print(list1.count(50))      #1
# print(list1.count(100))     #0
# print(list1.index(10))      #0
# print(list1.index(20))      #1

# list1.remove(10)
# print(list1)        #[20, 30, 40, 50, 60, 70, 80, 10, 20]

# list1.remove(40)
# print(list1)        #[20, 30, 50, 60, 70, 80, 10, 20]

# list1.remove(20)
# print(list1)        #[30, 50, 60, 70, 80, 10, 20]

# x = list1.pop()
# print(x)            # 20
# print(list1)        # [30, 50, 60, 70, 80, 10]

# y = list1.pop()
# print(y)            # 10
# print(list1)        # [30, 50, 60, 70, 80]



# list1 = [10,20,30,40,50]
# x = list1.pop(1)
# print(x)
# print(list1)


# list1 = [10,20,30,40,50]
# list1.clear()
# print(list1)

# list1 = [10,20,30,40,50]
# del list1[1]
# print(list1)


# list1 = [10,50,20,40,30]
# list1.sort()
# print(list1)
# sorted() & sort()
# sorted() - creates the new list
# sort() - wont creates the new list

# list1.sort(reverse=True)
# print(list1)


# list1 = [10,20,30,40,50]

# res1 = list1[::-1]
# print(res1)

# list1.reverse()
# print(list1)


# list1 = [10,20,30,40,50]
# list1[2] = 3000
# print(list1)        # mutable


# list1 = [10,20,30,40,50]
# list2 = [100,200,300,400,500]

# for element in list1:
#     print(element)

# for index,element in enumerate(list1):
#     print(index,element)

# for element1,element2 in zip(list1,list2):
#     print(element1,element2)


# list1 = [[1,2,3],
#          [4,5,6],
#          [7,8,9]]
# for inner in list1:
#     for index,element in enumerate(inner):
#         print(index,element,sep="--->")
#     print("-------")

# list1 = [[1,2,3],
#          [4,5,6],
#          [7,8,9]]
# list1[0][0] = 100
# list1[1][1] = 500
# list1[2][2] = 900
# print(list1)

# list1 = [10,20,30]
# list2 = [40,50,60]

# list1.extend(list2)
# print(list1)

# list3 = list1 + list2
# print(list3)

# list4 = list1 * 2
# print(list4)


# == (compare values and order)
# is comparing "memory location"
# list1 = [10,20,30]
# list2 = [10,20,30]
# list3 = [30,10,20]
# print(list1 == list2)
# print(list1 == list3)
# print(list1 is list2)

# l1 = [10,20]
# l2 = l1
# print(l1 is l2)

# numbers = [1,2,3,4,5]
# res = [num*num for num in numbers]
# print(res)

# numbers = [1,2,3,4,5,6]
# res = [n for n in numbers if n%2 == 0]
# print(res)


# list1 = [10,20,30]
# list2 = list1
# list1.append(40)
# print(list2)        # [10, 20, 30, 40]


# shallow copy
# list1 = [10,20,30]
# list2 = list1.copy()
# list1.append(40)
# print(list2)

# list1 = [10,20,30,40,50]
# element1,element2,element3,element4,element5 = list1
# print(element1,element2,element3,element4,element5)

# list1 = [10,20,30,40,50]
# element1, *list2, element2 = list1
# # list2 = [20,30,40]
# x,*y = list2
# a,b = y
# print(element1,x,a,b,element2)


# list1 = list("Python")
#               # ['P', 'y', 't', 'h', 'o', 'n']
# for ch in list1:
#     print(ch)

# any() - True

# list1 = [True,False,True,False,False]
# print(any(list1))

# list1 = [[],(),{},False,0,0.0,1]
# print(any(list1))


# all()
# list1 = [True,True,True,True,False]
# print(all(list1))


# list1 = [("Std1",80),
#          ("Anil",95),
#          ("Raju",70)]
# # list1.sort()
# # print(list1)

# list1.sort(key=lambda x:x[1])
# print(list1)


# list1 = [{"name":"Brijesh","marks":90},
#          {"name":"Anil","marks":70}]
# list1.sort(key=lambda x:x["name"])
# print(list1)

# list1.sort(key=lambda x:x["marks"])
# print(list1)
# collection of hetrogeneous elements called as "list"
# [] / list()
# positive(0)(left to right) & negative(-1)(right to left) indexes
# mutable

# Example-1
# list1 = [10,20,30,40,50]
# unpacking
# e1,e2,e3,e4,e5 = list1
# print(e1,e2,e3,e4,e5, sep=" | ")

# Assignment
# emps = ["e101","emp1",100000]
# unpack by using e_id,e_name and e_sal

# Example-2
# list1 = [10,20,30,40,50]
# e1,e2,*list2 = list1
# e3,e4,e5 = list2
# 


# Assignment
# emps = ["e101","emp1",100000]
# unpack by using e_id and craete new list contains "emp1",100000


# Example-3
# list1 = [10,20,30,40,50]
# e1,*list2,e5 = list1
# list2 = [20,30,40]
# e2,*list3 = list2
# list3 = [30,40]
# e3,*list4 = list3
# list4 = [40]
# e4 = list4
# print(e1,e2,e3,e4,e5, sep=" | ")


# Example-4
# list1 = [10,20,20,10,30,40]
# print(list1.count(10))
# print(list1.count(50))


# Example-5
# list1 = [10,50,20,40,30]
# print(max(list1))
# print(min(list1))
# print(sum(list1))
# print(len(list1))
# print(sum(list1) / len(list1))


# Example-6
# list1 = [10]
# list1.append(30)
# print(list1)            # [10, 30]
# list1.insert(1,20)
# print(list1)            # [10, 20, 30]
# list2 = [40,50]
# list1.extend(list2)
# print(list1)            # [10, 20, 30, 40, 50]

# list1.remove(10)
# print(list1)            # [20, 30, 40, 50]

# list1.pop()
# print(list1)

# list1.clear()
# print(list1)                # []

# del list1
# print(list1)


# Example-7
# list1 = [10,20,30,40,50]
# del list1[0]
# print(list1)        # [20, 30, 40, 50]

# list1.pop(0)
# print(list1)

# del list1
# try:
#     print(list1)
# except:
#     print("list1 not available in memory !!!")


# Example-8
# list1 = [10,20,30]
# list2 = [40,50]
# list1.append(list2)
# print(list1)        # [10,20,30,[40,50]]

# list1.extend(list2)
# print(list1)


# Example-9
# list1 = [10,20,30,40,50]
# print(30 in list1)
# print(300 not in list1)
# print(40 not in list1)


# Example-10
# list1 = [10,20,30,40,50]
# print(list1[::2])           # [10, 30, 50]      display only even index elements
# print(list1[::3])           # [10, 40]
# print(list1[::4])           # [10, 50]

# print(list1[::-1])          # [50, 40, 30, 20, 10]
# print(list1[::-2])
# print(list1[::-3])



# Example-11 (shallow copy)
# list1 = [10,20,30,40,50]
# list2 = list1
# list1.append(60)
# print(list2)            # [10, 20, 30, 40, 50, 60]



# Example-12 (deepcopy)
# import copy
# list1 = [10,20,30,40,50]
# list2 = copy.deepcopy(list1)

# list1[0] = 1000
# print(list2)


# Example-13
# list1 = [10,20,30]
# list2 = [10,20,30]
# list3 = [10,20,40]
# list1 = list2
# print(list1 == list2)
# print(list1 is list2)

# print(list1 == list3)
# print(list2 == list3)
# print(list1 is list3)
# print(list2 is list3)


# Example-14 (concatination)
# list1 = [10,20,30]
# list2 = [40,50,60]
# list3 = [*list1,*list2]
# print(list3)



# Example-14
# list1 = [10,20,30]
# list2 = [40,50,60]
# list3 = [*list1,*list2]
# print(list3)

# Example-15
# list1 = [10,20,30]
# list2 = [40,50,60]
# list3 = [e1+e2 for e1,e2 in zip(list1,list2)]
# print(list3)


# Example-16 (list2 must contain [10,20,30,40])
# list1 = [10,20,30,10,30,30,40]
# list2 = []
# for element in list1:
#     if list1.count(element) <= 1:
#         list2.append(element)

# print(list2)


# Example-17
# list1 = [10,20,30]
# list2 = list1 * 2
# print(list2)        # [10, 20, 30, 10, 20, 30]

# Example-18
list1 = [[10,20,30],
         [40,50,60],
         [70,80,90]]
for inner in list1:
    for element in inner:
        print(element)





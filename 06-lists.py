# Lists - collection of hetrogeneous and ordered values
# []
# index starts from 0 (Supports Negative Indexes)
# Allows Duplicates
# Mutable

# Example-1
# list1 = [10,20,30]
# print(list1)

# list2 = list((100,200,300))
# print(list2)

# list3 = list("Hello")
# print(list3)


# Example-2
# list1 = [100,200,300,400,500]
# print(list1[0], list1[-5])
# print(list1[2], list1[-3])
# print(list1[4], list1[-1])
# print(list1[0:2])
# print(list1[:3])
# print(list1[2:])
# print(list1[-3:-1])

# res = list1[::-1]
# print(res)
# print(list1)

# res1 = list1[::-2]
# print(res1)
# print(list1)

# res3 = list1[::-3]
# print(res3)
# print(list1)


# Example-4
# list1 = [10,20,30]
# list1.append(40)            #list1 = [10,20,30,40]

# list2 = [50,60]
# list1.extend(list2)         #list1 = [10,20,30,40,50,60]

# list1.insert(1,15)          #list1 = [10,15,20,30,40,50,60]

# list3 = [10,20]
# list1.extend(list3)         #list1 = [10,15,20,30,40,50,60,10,20]


# list1.remove(10)            # list1 = [15,20,30,40,50,60,10,20] 

# list1.pop()                 # list1 = [15,20,30,40,50,60,10] 

# list1.sort()                # list1 = [10,15,20,30,40,50,60]

# list1.sort(reverse=True)
# print(list1)

# Example - 5 (Shallow Copy)
# list1 = [10,20,30]
# list2 = list1
# list2.append(40)
# print(list1)

# list1 = [[10,20],[30,40]]
# list2 = list1
# list1[0][0] = 100
# print(list2)


# Example - 6 (deepcopy)
# import copy
# list1 = [[10,20],[30,40]]
# list2 = copy.deepcopy(list1)
# list1[0][0] = 100
# print(list2)


# Example-7
# list1 = [10,50,20,40,30,10,20]
# print(len(list1))
# print(max(list1))
# print(min(list1))
# print(sum(list1))
# print(sum(list1) / len(list1))
# print(list1.count(10))
# print(list1.count(50))
# print(list1.index(50))
# print(list1.index(20))

# list2 = sorted(list1)       # sort() and sorted()
# print(list2)
# print(list1)

list1 = [10,50,20,40,30,10,20]
# print( list1[ len(list1) // 2 ] )

x = 0
if 40 in list1:
    x = 40
print(x)
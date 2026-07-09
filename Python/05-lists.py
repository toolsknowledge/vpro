# list - collection of elements
# ordered
# mutable
# []
# allows duplicates
# hetrogeneous

# list1 = [1,2,3]
# list2 = list1.copy()  # list2 = list(list1)


# list1 = [1,2,3]
# list2 = list1 # ref copy



# Nested List
# list1 = [[1,2,3],
#          [4,5,6],
#          [7,8,9]]
# print(list1[0][0])
# print(list1[1][1])
# print(list1[2][2])

# for inner_list in list1:
#     for i in range(len(inner_list)):
#         print(i,inner_list[i])



# Comprehension
# squares = [i*i for i in range(5)]
# print(squares)

# Loop
# list1 = [10,20,30,40,50]
# for element in list1:
#     print(element,end=" ")

# for i in range(len(list1)):
#     print(i, list1[i])

# Example-7
# list1 = [10,50,20,40,30]
# list1.sort()
# list1.sort(reverse=True)
# print(list1)
# list2 = sorted(list1)
# print(list2)
# print(list1)

# Example-6
# list1 = [1,2,3,2,2]
# print(list1.index(2))
# print(list1.count(2))


# Example-5
# list1 = [1,2,3,2]
# list1.remove(2)
# list1.pop()
# list1.pop(1)
# list1.clear()
# print(list1)


# Example-4
# list1 = [1,2]
# list1.append(3)
# list2 = [4,5]
# list1.extend(list2)
# list1.insert(1,99)
# print(list1)


# Example-3 (mutable) (change)
# list1 = [1,2,3,4,5]
# list1[0] = 1000
# print(list1)


# Example-2
# list1 = [10,20,30,40,50,60,70,80,90,100]
# print(list1[0],list1[-10])
# print(list1[0:3])
# print(list1[-10:-7])
# print(list1[7:])
# print(list1[::-1])

# Example-1
# list1 = []
# list2 = [10,20,30,40,50]
# list3 = [10,"Hello",True,10.1]
# list4 = list("Hello")
# list5 = list(range(5))
# print(f"Empty List :{list1}")
# print(f"Number List :{list2}")
# print(f"Hetrogeneous List :{list3}")
# print(f"Character List :{list4}")
# print(f"Number List :{list5}")
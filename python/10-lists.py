"""
    lists
    *****
        collection of "hetrogeneous" elements
        [] / list()
        index starts from "0"
        supports "negative" indexes
        lists are "mutable"
"""

# Example-1
# list1 = [10,20,30,40,50]
# 10 - 0
# 30 - "-3"
# 50 - "-1"
# 20 - 1
# print(list1[0])
# print(list1[-3])
# print(list1[-1])
# print(list1[::2])
# print(list1[::3])
# print(list1[::-1])
# print(list1[::-2])
# print(list1[::-3])
# print(list1[0:3])       # 0,1,2 included and "3 excluded"
# print(list1[:2])        # 0:2, 0,1 included and "2 excluded"
# print(list1[:1+1+1+1])  # 0:4, 0,1,2,3 included and "4 excluded"
# print(list1[-2:])
# print(list1[-4:])
# print(list1[-5:-2])


# Example-2
# list1 = [10,50,20,40,30]
# print(len(list1))
# print(max(list1))
# print(min(list1))
# print(sum(list1))
# print(sum(list1) / len(list1))

# res = sorted(list1)     # immutable function
# print(res)  # res = ascending order [10, 20, 30, 40, 50]
# print(list1)    # [10, 50, 20, 40, 30]

# list1.sort()    # mutable
# print(list1)    # [10, 20, 30, 40, 50] 


# Example-3
# list1 = [10,20,30,40,50]

# print(30 in list1)
# print(300 in list1)
# print(200 not in list1)

# numb = input("Enter Number :")
# found = False
# for element in list1:
#     if element == int(numb):
#         found = True
        
   
# res = "Found" if found else "Not Found"
# print(res) 


# Example-4
# list1 = [10,20,30,40,50]
# # print(list1[::-1])

# # list1.reverse()
# # print(list1)

# res = []
# for i in range(len(list1)-1,-1,-1):     # 4 included, -1 excluded and -1
#     res.append(list1[i])

# print(res)

# range(4,-1,-1)      # 4 included, -1 excluded, and step:-1



# Example-5 (mutable)
# list1 = [10,20,30,40,50]
# list1[0] = 1000
# print(list1)


# Example-6
# list1 = [10,20,30,40,50]
# for element in list1:
#     print(element)

# list2 = [[10,20,30],
#          [40,50,60],
#          [70,80,90]]
# for inner in list2:
#     for element in inner:
#         print(element)


# Example-7
# list1 = [10,30,40]
# list1.insert(1,20)  # [10,20,30,40]

# list2 = [50,60]
# list1.extend(list2) # [10,20,30,40,50,60]

# list1.append(70)    # [10,20,30,40,50,60,70]

# list1.remove(10)    # [20,30,40,50,60,70]

# list1.pop(4)        # [20,30,40,50,70]

# del list1[0]        # [30,40,50,70]

# print(list1)


# Example-8 (list comprehension)
# list1 = [1,2,3,4,5]
# res = [element*element for element in list1]
# print(res)

# Example-9
# list1 = [1,2,3,4,5]
# res = [element for element in list1 if element%2 == 0]
# print(res)
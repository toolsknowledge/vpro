# list1 = [10,20,30]
# list2 = list1.copy()
# list1.append(40)
# print(list2)


# list1 = [10,20]
# list2 = [30,40]
# list1.append(list2)
# print(list1)    # [10,20,[30,40]]

# list1.extend(list2)
# print(list1)

# print( [1] * 3 )
# print( [[]]*3 ) 

# list1 = [[]] * 3
# list1[0].append(100)   
# print(list1)


# list1 = [1,2,3,4,5]
# print(list1)
# for x in list1:
#     if x % 2 == 0:
#         list1.remove(x)

# print(list1)

# list1 = [10,30,20]
# list1.sort()
# print(list1)
# list2 = sorted(list1)
# print(list2)

# list1 = [10,20,30,10,20,30,40]
# for loop (remove duplicates)

# result = []
# for element in list1:
#     if element not in result:
#         result.append(element)

# print(result)

# result = []
# for element in list1:
    # if list1.count(element) == 1:
    #     result.append(element)

#     if result.count(element) == 0:
#         result.append(element)

# print(result)


# t1 = ("Hello")
# print(type(t1))

# t2 = ("Hello",)
# print(type(t2))

# t3 = tuple("Hello")
# print(type(t3))
# print(t3)

# list1 = list("Hello")
# print(type(list1))
# print(list1)


res = lambda s:len(s)
print( res("Hello") )


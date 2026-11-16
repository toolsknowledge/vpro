# Set - never allows "duplicates"
# {} / set() constructor
# unordered, Ex. 10,20,30 --> 20,10,30
# hetrogeneous

# Example-1
# s1 = {}
# print(type(s1))

# s2 = set()
# print(type(s2))


# Example-2
# s1 = {10,20,30,10,20,40}
# print(s1)

# s2 = {"VPro","VPro","vpro"}
# print(s2)

# s3 = {1,1.0,True}
# print(s3)

# list1 = [10,20,30,10,20,30,40]
# s4 = set(list1)
# print(s4)

# t1 = (10,20,30,10,20,40,30)
# s5 = set(t1)
# print(s5)


# Example-3
# s1 = {10,20,30}
# s1.add(40)
# print(s1)

# list1 = [50,60]
# s1.update(list1)
# print(s1)

# s1.remove(10)
# print(s1)

# s1.remove(10)
# s1.discard(10)

# x = s1.pop()
# print(x)

# s1.clear()
# print(s1)

# del s1
# print(s1)


# Example-4
# s1 = {10,20,30}
# print(20 in s1)
# print(200 not in s1)
# print(100 in s1)


# Example-5
# s1 = {10,20,30}
# for element in s1:
#     if element == 20:
#         s1.remove(element)
#         s1.add(200)

# print(s1)

# Example-6
# s1 = {1,2,3}
# s2 = {3,4,5}
# print(s1.union(s2))     # {1, 2, 3, 4, 5}       # union
# s3 = s1 | s2
# print(s3)               # {1, 2, 3, 4, 5}


# s4 = s1.intersection(s2)        # intersection
# print(s4)               # {3}

# s5 = s1 & s2
# print(s5)


# s3 = s1 - s2
# print(s3)
# s3 = s2 - s1
# print(s3)

# s3 = s1.difference(s2)
# print(s3)
# s3 = s2.difference(s1)
# print(s3)


# s3 = s1.symmetric_difference(s2)
# print(s3)       # {1, 2, 4, 5}

# s3 = s1 ^ s2
# print(s3)


# Example-7
# s1 = {1,2}
# s2 = {1,2,3,4}
# print(s1.issubset(s2))
# print(s2.issuperset(s1))


# Example-8
# s1 = {1,2,3}
# s2 = {4,5,6}
# print(s1.isdisjoint(s2))


# Example-9
# s1 = {10,20,30}
# print(len(s1))


# Example-10
# s1 = {1,2,3,4,5}
# s2 = {num*num for num in s1}
# print(s2)


# Example-11
# s1 = {10,20,30}
# s2 = {100,200,300}
# print(s2 < s1)
"""
    set
    ***
        never allows duplicates
        {} / set()
        hetrogeneous elements
        unordered
"""

# Example-1
# s1 = {}
# print(type(s1))

# s2 = set()
# print(type(s2))


# Example-2
# s1 = {10,20,10,30,40,10}
# print(s1)

# s2 = {"ravi","ravi","Ravi"}
# print(s2)

# s3 = set([10,20,10,30,10])
# print(s3)

# s4 = set((10,20,10,30,10))
# print(s4)

# Example - 3
# s1 = {10,20,30}
# s1.add(40)
# print(s1)

# s1.update([50,60])
# print(s1)

# s1.update((70,80))
# print(s1)       # {10,20,30,40,50,60,70,80}

# s1.remove(10)
# print(s1)       #{20,30,40,50,60,70,80}

# # s1.remove(10)     # Err
# # s1.discard(10)    # no err

# x = s1.pop()        
# print(x)

# s1.clear()
# print(s1)

# del s1
# print(s1)


# Example-4
# s1 = {1,2,3}
# s2 = {3,4,5}

# union
# s3 = s1.union(s2)
# print(s3)

# s3 = s1 | s2
# print(s3)

# s3 = s1.intersection(s2)
# print(s3)       # {3}

# s3 = s1 & s2
# print(s3)

# s3 = s1.difference(s2)
# print(s3)

# s3 = s2.difference(s1)
# print(s3)

# s3 = s1 - s2
# print(s3)

# s3 = s2 - s1
# print(s3)

# s3 = s1.symmetric_difference(s2)
# print(s3)

# s3 = s1 ^ s2
# print(s3)

# union, intersection, difference, symmetric_difference

# Example-5
# s1 = {1,2}
# s2 = {1,2,3,4}
# print(s1.issubset(s2))
# print(s2.issuperset(s1))

# Example-6
# s1 = {1,2,3}
# s2 = {111,11,4}
# print(s1.isdisjoint(s2))


# Example-7
# s1 = {10,20,30,40,50}
# for element in s1:
#     print(element)

# Example-8
s1 = {10,20,30,40,50}
print(len(s1))
print(max(s1))
print(min(s1))


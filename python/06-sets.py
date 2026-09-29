"""
    set
    ***
        set never allows duplicates
        {} / set() constructor
        unordered
        while modifying element set is immutable
        whole set iteself is mutable
"""

# s1 = {10,20,30,10,20}
# print(s1)         # {10, 20, 30}


# Empty Set
# s1 = {}
# print(type(s1))
# s2 = set()
# print(type(s2))

# Example-3
# s1 = {"ravi","Ravi","ravi",1,1.0,True}
# print(s1)

# Example-4
# s1 = set([10,20,30,10,20,40])
# print(s1)

# s2 = set(("python","python","agenticai"))
# print(s2)


# # Example-5
# s1 = {10,20,30}
# s1.add(40)
# print(s1)       # {40, 10, 20, 30}
# s1.update([60,70])
# print(s1)      # {70, 40, 10, 20, 60, 30}
# s1.update((80,90))
# print(s1)       # {70, 40, 10, 80, 20, 90, 60, 30}


# # Example-6
# s1 = {10,20,30}
# s1.remove(30)
# print(s1)

# # s1.remove(30)
# # s1.discard(30)

# s1.pop()    # removes one random element
# print(s1)

# s1.clear()
# print(s1)


# # Example-7
# s1 = {10,20,30}
# print(20 in s1)
# print(200 not in s1)


# # Example-8
# s1 = {10,20,30}
# for element in s1:
#     if element == 20:
#         s1.remove(element)
#         s1.add(200)
# print(s1)


# # Example-9 (union)
# s1 = {1,2,3}
# s2 = {3,4,5}
# # s3 = s1.union(s2)
# # print(s3)             # {1, 2, 3, 4, 5}
# s3 = s1 | s2
# print(s3)               # {1, 2, 3, 4, 5}


# # Example-10 (intersection)
# s1 = {1,2,3}
# s2 = {3,4,5}
# # s3 = s1.intersection(s2)
# # print(s3)                   # {3}

# s3 = s1 & s2
# print(s3)


# Example - 11 (difference) (<5sec copilot/claude/cursor)
# s1 = {1,2,3}
# s2 = {3,4,5}
# s3 = s1.difference(s2)
# print(s3)

# s4 = s2.difference(s1)
# print(s4)

# # Example - 12
# s1 = {1,2,3}
# s2 = {3,4,5}
# # s3 = s1.symmetric_difference(s2)
# # print(s3)           # {1, 2, 4, 5}

# s3 = s1 ^ s2
# print(s3)


# Example-13
# s1 = {1,2}
# s2 = {1,2,3,4}
# print(s1.issubset(s2))
# print(s2.issuperset(s1))

# # Example-14
# s1 = {1,2,3}
# s2 = {4,5,6}
# s3 = {1,2,3}
# print(s1.isdisjoint(s2))
# print(s1.isdisjoint(s3))


# Example-15 (set compression)
# s1 = {1,2,3,4,5}
# res = {num**num for num in s1}
# print(res)


# Example-16
# s1 = {10,20,30,40,50}
# print(len(s1))
# print(sum(s1))
# print(max(s1))
# print(min(s1))
# print(sum(s1) / len(s1))








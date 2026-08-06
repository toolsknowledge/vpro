# set - never allows duplicates, allows hetrogeneous, unordered, {} / set() , mutable

# Example-1
# s1 = {10,20,10,20,30}
# print(s1)
# s2 = set([10,20,10,20,30])
# print(s2)
# s3 = {}
# print(type(s3))
# s4 = set()
# print(type(s4))
# s5 = set((10,20,10))
# print(s5)


# Example-2
# s1 = {10,20}
# s1.add(30)
# s1.update([40,50])
# s1.update((60,70))
# s1.remove(10)
# s1.remove(100)
# s1.discard(100)
# s1.pop()
# s1.clear()
# print(s1)

# Example-3
# s1 = {10,20,30}
# print(20 in s1)
# print(40 not in s1)
# print(200 in s1)

# Example-4
# s1 = {1,2,3}
# s2 = {3,4,5}

# print(s1.union(s2))   # {1,2,3,4,5}
# print(s1 | s2)

# print(s1.intersection(s2))  # {3}
# print(s1 & s2)                 

# print(s1 - s2)  # {1,2}
# print(s2 - s1)

# print(s1 ^ s2)      # {1, 2, 4, 5}

# Example-5
# s1 = {1,2,3}
# s2 = {1,2}
# print(s1.issuperset(s2))
# print(s2.issuperset(s1))

# print(s2.issubset(s1))
# print(s1.issubset(s2))

# Example - 6
# frozenset (wont allows any operation)
# f1 = frozenset([10,20,30])
# print(f1)
# f1.update([40,50])

# Example - 7
# s1 = {1,1.0,True}
# print(s1)

# Example - 8
# s1 = {10,20,30,40,50}
# for element in s1:
#     print(element)


# Example - 9
# s1 = {10,20,30,40,50}
# print(len(s1))


# Example - 10
s1 = {(10,20)}      # set - never allows non-hashables
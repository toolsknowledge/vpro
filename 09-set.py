# Set - 1) Not Ordered, 2) Mutable 3) No Duplicates , 4) No Indexing, 5) Allows Hetrogeneous, 6) {} / set(), 7) No Slicing 8) Search, 9) Hashing

# FAQ3 
# s1 = {10,20,50,40,30}
# print(s1)
# print(len(s1))
# print(max(s1))
# print(min(s1))
# print(sum(s1))
# print(sorted(s1))


# FAQ2
# s1 = {1,True,1.0}
# print(s1)

# FAQ1
# s1 = set("Hello")
# print(s1)


# Example - 9
# s1 = frozenset([1,2])
# print(type(s1))



# Example - 8
# res = {x*x for x in range(5)}
# print(res)



# Example - 7
# s1 = {10,20,30,40,50}
# for element in s1:
#     print(element)

# s2 = {{10,20},{30,40}}
# for inner_set in s2:        # Err
#     print(inner_set)

# Example - 6
# s1 = {10,20,30,40,50}
# print(20 in s1)
# print(20 not in s1)


# Example - 5
# s1 = {1,2,3}
# s2 = {3,4,5}
# print(s1.union(s2))
# print(s1 | s2)

# print(s1.intersection(s2))
# print(s1 & s2)

# print(s1.difference(s2))
# print(s1-s2)
# print(s2.difference(s1))
# print(s2-s1)

# print(s1.symmetric_difference(s2))
# print(s1 ^ s2)



# Example - 4
# s1 = {1,2,3}
# s1.add(4)
# list1 = [5,6,7,8]
# s1.update(list1)
# tuple1 = (9,10)
# s1.update(tuple1)

# s1.remove(10)
# s1.remove(100)
# s1.discard(100)

# s1.pop()
# s1.clear()
# print(s1)


# Example - 3
# s1 = {10,20,30}
# print(s1[0]) # Err


# Example - 2
# s1 = {10,20,10,20,30}
# print(s1)

# list1 = [10,20,10,20,30]
# s2 = set(list1)
# print(s2)

# tuple1 = (10,10,20,30,20)
# s3 = set(tuple1)
# print(s3)



# Example - 1
# s1 = {}
# print(type(s1))

# s2 = set()
# print(type(s2))
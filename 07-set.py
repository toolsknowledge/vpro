"""
    set - never allows duplicates
    {} / set()
    unordered
"""

# s1 = {10,20,30,10,20,40}
# print(s1)

# s1 = {"Ravi","Ravi","ravi"}
# print(s1)

# list1 = [10,20,30,10,20]
# res = list( set(list1) )
# print(res)

# tuple1 = (10,20,10)
# print( tuple( set(tuple1) ) )


# s1 = {}
# print(type(s1))

# s2 = set()
# print(type(s2))


# add() - adding element to set
# update() - adding list/tuple to set
# remove() - remove element (Err)
# discard() - remove element (No Exception)
# clear() - remove all elements 

# s1 = {10,20}
# s1.add(30)          # {10,20,30}

# list1 = [40,50,60]
# s1.update(list1)    # {10,20,30,40,50,60}

# s1.remove(10)       # {20,30,40,50,60}
# # s1.remove(100)    # Err
# s1.discard(100)     # No Err

# x = s1.pop()            # {40, 50, 20, 60}
# print(x)

# s1.clear()
# print(s1)


# s1 = {1,2,3}
# s2 = {3,4,5}

# print(s1.union(s2))
# print(s2.union(s1))
# print(s1 | s2)

# print(s1 & s2)
# print(s1.intersection(s2))
# print(s2.intersection(s1))

# print(s1 - s2)
# print(s2 - s1)
# print(s1.difference(s2))
# print(s2.difference(s1))

# print(s1.symmetric_difference(s2))
# print(s2.symmetric_difference(s1))
# print(s1^s2)
# print(s2^s1)

# s1 = {1,2,3}
# s2 = {1,2}

# print(s2.issubset(s1))
# print(s2 <= s1)

# print(s1.issuperset(s2))
# print( s1 >= s2 )

# s3 = {1,2,3}
# s4 = {4,5,6}
# print(s3.isdisjoint(s4))


# s1 = {10,20,30,40,50,60}
# print(len(s1))
# print(30 in s1)
# print(300 not in s1)


# s1 = {1,2,3,4,5}

# res = set()
# for element in s1:
#     res.add(element*element)
# print(res)

# print( {element*element for element in s1} )

# print( { element**element for element in s1 if element%2 == 0 } )


"""
    list
    ****
        collection of "ordered","indexed" and "hetrogeneous" elements
        list is a "mutable"
        "[]" / "list()"
        allows "duplicates"
        list supports both "positive/negative" indexes
"""
# Example-1
# list1 = [10,20,30,40,50]
# list2 = list((10,20,30,40,50))
# list3 = list("Python")
# print(list1)
# print(list2)
# print(list3)

# Example-2
# list1 = [10,20,30,40,50]
# print(list1[0:2])
# print(list1[:3])
# print(list1[2:])
# print(list1[:0+1])  
# print(list1[-5])
# print(list1[-2:]) 
# print(list1[-3:-1])   
# print(list1[::-1])
# print(list1[::-2])
# print(list1[::-3])

# Example-3
# list1 = [10,20]
# list1.append(30)

# list2 = [40,50]
# list1.extend(list2)     

# list1.insert(2,25)
# list1.append(10)
# list1.remove(10)
# list1.pop()
# list1.clear()
# print(list1)

# Example-4
# list1 = [10,50,20,40,30]
# list1.sort()
# print(list1)

# list1.sort(reverse=True)
# print(list1)

# list2 = [10,20,30]
# list2.reverse()
# print(list2)


# Example-5
# list1 = [10,20,30]
# list2 = list1
# list2.append(40)
# print(list1)

# list1 = [10,20,30]
# list2 = list1.copy()
# list2.append(40)
# print(list1)


# Example-6
# print( [x for x in range(5)] )
# print( [x for x in range(10) if x%2 == 0] )


# Faq-1
# list1 = [1,2,3]
# list2 = list1
# list1 = list1 + [4]
# print(list2)
# print(list1)

# Faq-2
# list1 = [10,20,30]
# print(list1 * 3)

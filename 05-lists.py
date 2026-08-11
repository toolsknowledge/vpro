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

# list1 = [1,2,3,1,1,2,4,3]
# print(list1.count(1))
# print(list1.count(2))
# print(list1.count(5))


# list1 = [1,2,3,1,1,2,4,3]
# print( list( set( [x for x in list1 if list1.count(x)>1] )) )

# nums = [10,50,20,40,30]
# print(max(nums))
# print( sorted(nums)[-2] )


# res =  [[] for _ in range(3)] 
# res[0].append(10)
# print(res)

# list1 = [100,200,300,400,500]
# for index,element in enumerate(list1):
#     print(index,element)

# list1 = [1,2,3,4,5]
# list2 = ["Python","ML","DL","NLP","GenAI"]
# for element1,element2 in zip(list1,list2):
#     print(element1,element2)


# print( 
#     list( map(lambda num1:num1*100,[1,2,3,4,5]) ) 
#     )

# print( tuple( filter(lambda num1:num1>=300,(100,200,300,400,500)) ) )

# from functools import reduce
# res = reduce(lambda num1,num2:num1+num2,(1,2,3,4,5))
# res1 = (res,)
# print(res1)
 



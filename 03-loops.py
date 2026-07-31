"""
    loops - execute block of code multiple times, then we will use loops 
    Python supports below loops
    1) for
    2) while  
"""
# Example-1
# for element in range(5):
#     print(element)

# for element in range(2,7):
#     print(element)

# for element in range(0,10,2):
#     print(element)

# for element in range(1,10,2):
#     print(element)

# for element in range(10,0,-1):
#     print(element)

# for element in range(10,1,-2):
#     print(element,end=" ")


# Example - 2
# list1 = [10,20,30,40,50]
# list2 = ["Python","ML","DL","NLP","GenAI"]

# for element in list1:
#     print(element)

# for a,b in enumerate(list1):
#     print(a,b,sep="--->")

# for element1,element2 in zip(list1,list2):
#     print(element1,element2,sep="---->")

# t1 = 10,20,30,40,50
# for element in t1:
#     print(element)


# s1 = {10,20,30,10,20}
# for element in s1:
#     print(element)


# for index,element in enumerate(s1):
#     print(index,element,sep="---->")


# d1 = {
#     "EmpID" : 101,
#     "EmpName" : "Emp1",
#     "EmpSal" : 10000
# }
# for key in d1.keys():
#     print(key)

# for values in d1.values():
#     print(values)

# for key,value in d1.items():
#     print(key,value)


# for i in range(3):
#     for j in range(3):
#         print([i,j])


# for i in range(1,11):
#     for j in range(1,11):
#         print(f"{i} x {j} = {i*j}")
#     print("-----------------")


# i = 1
# while i<=5:
#     print(i)
#     i = i+1



# i = 5
# while i>=1:
#     print(i)
#     i = i-1


# i=1
# while i<=5:
#     if i==3:
#         break
#     print(i)
#     i = i+1

i = 1
while i <= 5:
    if i == 3:
        i = i + 1
        continue
    print(i)
    i = i + 1









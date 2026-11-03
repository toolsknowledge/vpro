# list1 = [10,20,30,40,50]

# for element in list1:
#     print(element)

# list1 = [100,200,300,400,500]
# for element in list1:
#     print(element,end=" | ")


# list1 = ["Python","ML","DL","NLP","GenAI","AgenticAI"]
# for index,element in enumerate(list1):
#     print(index,element,sep="---->")

# 0 -- Python
# 1 -- ML
# 2 -- DL

# list1 = [10,20,30,40,50]
# list2 = [100,200,300,400,500]
# for element1,element2 in zip(list1,list2):
#     print(element1,element2,sep="--->")


# for i in range(10):     # 0 included and 10 excluded
#     print(i,end=" ")   


# for i in range(1,10):       # starts with 1 end with 9
#     print(i)


# for i in range(0,10,2):         # 0  2. 4.  6.  8
#     print(i,end=" ")


# for i in range(10,0,-2):        # 10 8 6 4 2
#     print(i)


# for i in range(10):
#     if i == 5:
#         # break                 # 0 1 2 3 4
#         continue                # 0 1 2 3 4 6 7 8 9
#     print(i)


# for i in range(5):
#     print(i)
# else:
#     print("for loop completed !!!")

# for i in range(5):
#     if i == 3:
#         break
#     print(i)
# else:
#     print("for loop completed !!!")


# for i in range(5):
#     if i == 2:
#         break
#     print(i)                # 0 1 2 3 4
# else:
#     print("Hello")


# i = 1       # initilization
# while i<=5:     # 1 <= 5
#     print(i)    # 1  2. 3.  4.  5   
#     i += 1      # i = 2        



# for i in range(3):
#     for j in range(2):
#         print(i,j)      # 0 0 0 1
#                         # 1 0 1 1
#                         # 2 0 2 1


# day = 1
# match day:
#     case 1:
#         print("Monday !!!")
#     case 2:
#         print("Tuesday !!!")
#     case _:
#         print("No Day !!!")


# list1 = [10,"Hello",True,1.0,100.12345]
# iterate with for loop and while loop
# iterate with enumerate() also


# Nested List
list1 = [[10,20,30],
         [40,50,60],
         [70,80,90]]
for x in list1:
    for element in x:
        print(element)

